import sys
import json as json
import ast

def PrintUsage():
    sys.stderr.write("""
Usage:
    parse_python.py <file>
""")
    exit(1)

def read_file_to_string(filename):
    with open(filename, 'rt', encoding='utf-8') as f:
        return f.read()

def parse_file(filename):
    tree = ast.parse(read_file_to_string(filename), filename)
    
    json_tree = []
    def gen_identifier(identifier, node_type='identifier'):
        pos = len(json_tree)
        json_node = {}
        json_tree.append(json_node)
        json_node['type'] = node_type
        json_node['value'] = identifier
        return pos

    def traverse_list(l, node_type='list'):
        pos = len(json_tree)
        json_node = {}
        json_tree.append(json_node)
        json_node['type'] = node_type
        children = [traverse(item) for item in l]
        if children:
            json_node['children'] = children
        return pos

    def traverse(node):
        pos = len(json_tree)
        json_node = {}
        json_tree.append(json_node)
        json_node['type'] = type(node).__name__
        children = []

        if isinstance(node, ast.Name):
            json_node['value'] = node.id
        elif isinstance(node, ast.Constant):  # Python 3.8+
            json_node['value'] = str(node.value)
        elif isinstance(node, ast.alias):
            json_node['value'] = node.name
            if node.asname:
                children.append(gen_identifier(node.asname))
        elif isinstance(node, ast.FunctionDef):
            json_node['value'] = node.name
        elif isinstance(node, ast.ClassDef):
            json_node['value'] = node.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                json_node['value'] = node.module
        elif isinstance(node, ast.Global):
            for n in node.names:
                children.append(gen_identifier(n))
        elif isinstance(node, ast.keyword):
            json_node['value'] = node.arg

        if isinstance(node, ast.For):
            children.extend([traverse(node.target), traverse(node.iter)])
            children.append(traverse_list(node.body, 'body'))
            if node.orelse:
                children.append(traverse_list(node.orelse, 'orelse'))
        elif isinstance(node, (ast.If, ast.While)):
            children.append(traverse(node.test))
            children.append(traverse_list(node.body, 'body'))
            if node.orelse:
                children.append(traverse_list(node.orelse, 'orelse'))
        elif isinstance(node, ast.With):
            for item in node.items:
                children.append(traverse(item.context_expr))
                if item.optional_vars:
                    children.append(traverse(item.optional_vars))
            children.append(traverse_list(node.body, 'body'))
        elif isinstance(node, ast.Try):
            children.append(traverse_list(node.body, 'body'))
            children.append(traverse_list(node.handlers, 'handlers'))
            if node.orelse:
                children.append(traverse_list(node.orelse, 'orelse'))
            if node.finalbody:
                children.append(traverse_list(node.finalbody, 'finalbody'))
        elif isinstance(node, ast.arguments):
            children.append(traverse_list(node.args, 'args'))
            children.append(traverse_list(node.defaults, 'defaults'))
            if node.vararg:
                children.append(gen_identifier(node.vararg.arg, 'vararg'))
            if node.kwarg:
                children.append(gen_identifier(node.kwarg.arg, 'kwarg'))
        elif isinstance(node, ast.ExceptHandler):
            if node.type:
                children.append(traverse_list([node.type], 'type'))
            if node.name:
                children.append(gen_identifier(node.name, 'name'))
            children.append(traverse_list(node.body, 'body'))
        elif isinstance(node, ast.ClassDef):
            children.append(traverse_list(node.bases, 'bases'))
            children.append(traverse_list(node.body, 'body'))
            children.append(traverse_list(node.decorator_list, 'decorator_list'))
        elif isinstance(node, ast.FunctionDef):
            children.append(traverse(node.args))
            children.append(traverse_list(node.body, 'body'))
            children.append(traverse_list(node.decorator_list, 'decorator_list'))
        else:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.expr_context, ast.operator, ast.boolop, ast.unaryop, ast.cmpop)):
                    json_node['type'] += type(child).__name__
                else:
                    children.append(traverse(child))

        if isinstance(node, ast.Attribute):
            children.append(gen_identifier(node.attr, 'attr'))

        if children:
            json_node['children'] = children
        return pos

    traverse(tree)
    return json.dumps(json_tree, separators=(',', ':'), ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        PrintUsage()
    try:
        print(parse_file(sys.argv[1]))
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
