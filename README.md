# Python Code Complexity Classification Using AST & Graph Neural Networks

A deep learning project for **automatically classifying the complexity of Python source code** based on its Abstract Syntax Tree (AST) representation using **Graph Neural Networks (GNN)** (specifically GCN and GAT).  
This repository contains data processing pipelines, model training/evaluation scripts, and illustrative notebooks for the Python150k dataset.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Motivation & Objectives](#motivation--objectives)
- [Dataset & Preprocessing](#dataset--preprocessing)
- [Model Architecture](#model-architecture)
- [How to Run](#how-to-run)
- [Results](#results)
- [Limitations & Future Work](#limitations--future-work)
- [Team](#team)

---

## Project Overview

This project leverages **Graph Neural Networks** (GNNs) to classify Python code snippets into complexity levels, using the code's structural information derived from its **AST**.  
The models are trained and evaluated on the large-scale Python150k dataset, aiming to build a foundation for automated code assessment, complexity analysis, and quality assurance in software development.

---

## Motivation & Objectives

### Why this topic?

- Traditional complexity metrics (e.g., cyclomatic complexity) often require manual inspection or handcrafted features, limiting automation and scalability.
- GNNs can directly exploit code structure by modeling the AST as a graph, learning rich representations for classification tasks.

### Main goals

- Build an end-to-end pipeline for **multi-class AST classification** using GCN and GAT architectures.
- Compare performance of GCN vs. GAT on real-world Python code (Python150k).
- Provide tools and insights for practical applications in code quality analysis and automated code review.

---

## Dataset & Preprocessing

- **Dataset:** [Python150k](https://www.sri.inf.ethz.ch/py150) (open-source, ~150,000 ASTs from open Python projects)
  - Training: 100,000 ASTs (`python100k_train.json`)
  - Evaluation: 50,000 ASTs (`python50k_eval.json`)
- **AST Format:** Each AST is a JSON list, where each node has:
  - `type`: syntactic category (e.g. Module, Assign, Call, Name, Num, etc.)
  - `value`: literal value (optional)
  - `children`: list of child node indices
- **Labeling:**  
  ASTs are labeled into 3 classes based on their size:
  - **Class 0:** Small AST (< 20 nodes)
  - **Class 1:** Medium AST (20–49 nodes)
  - **Class 2:** Large AST (≥ 50 nodes)
- **Preprocessing steps:**
  - Convert JSON ASTs to undirected graphs (using NetworkX / PyTorch Geometric)
  - One-hot encode node types as features
  - Balance classes via over/undersampling as needed

---

## Model Architecture

- **Graph Neural Networks:**  
  - **GCN (Graph Convolutional Network):** Aggregates features from neighbors equally, suitable for extracting local and global structural patterns.
  - **GAT (Graph Attention Network):** Applies attention mechanism, learning dynamic weights for neighbor aggregation and emphasizing important syntactic structures.
- **Pooling:** Global mean pooling for graph-level embedding
- **Classifier:** Fully-connected (MLP) output layer for 3-way classification
- **Frameworks:** PyTorch, PyTorch Geometric, NetworkX

---

## How to Run

### 1. Install dependencies

pip install torch torch_geometric networkx tqdm

---

## 2. Notebooks

- **Visualize-data.ipynb**: Data loading, preprocessing, and exploratory visualization  
- **Model.ipynb**: Model definition, training, and evaluation (GCN/GAT)

---

## 3. Usage

- Update data paths in the notebook if needed
- Run all cells in order
- Review results, plots, and confusion matrices

---

## Results

- **Overall test accuracy:** ~83.6% (on >3,600 test samples)
- **Best performance:**
  - Small ASTs: 92.0% accuracy
  - Large ASTs: 92.3% accuracy

**Key insights:**
- Multi-head attention in GAT captures diverse syntactic patterns
- Most misclassifications occur for ASTs near class boundaries (e.g., 45–55 nodes)
- Attention weights highlight meaningful control-flow and structural nodes

---

## Limitations & Future Work

**Current limitations:**
- Medium-sized ASTs are harder to classify (class confusion near size boundaries)
- Only node types are used as features; richer features could improve performance

**Future directions:**
- Incorporate additional structural features (e.g., depth, centrality)
- Test other GNN architectures (GraphSAGE, GIN, etc.)
- Extend to other programming languages or tasks (bug detection, code summarization)

---

## Team

- **Hoang Bao Long** – 22520807  
- **Dang Tran Long** – 22520805  
- **Luong Tuan Vy** – 22521711  
- **Nguyen Duy Phuong** – 22521165

**Advisor:** Mr. Ha Le Hoai Trung  
University of Information Technology – VNU HCMC

---

For further details, see `HoangBaoLong_DangTranLong_NguyenDuyPhuong_LuongTuanVy_22520807_22520805_22521165_22521711.pdf` and the slide deck included in this repository.  
Check out the notebooks to experiment with data and models directly.
