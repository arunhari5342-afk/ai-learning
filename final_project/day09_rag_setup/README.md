# Day 09 — RAG Setup

## Objective

Set up PostgreSQL with pgvector and perform basic vector similarity
search for the final RAG project.

## Topics Covered

- Vector databases
- PostgreSQL pgvector
- Vector columns
- Embeddings
- JSONB metadata
- Cosine distance
- Nearest-neighbour search
- HNSW indexing
- Query plans
- RAG database design

## Database Table

### embeddings

| Column | Type | Description |
|---|---|---|
| id | SERIAL | Primary key |
| content | TEXT | Document/chunk content |
| embedding | VECTOR(4) | Vector representation |
| metadata | JSONB | Additional document information |

## Similarity Search

The pgvector cosine distance operator is:

`<=>`

Smaller cosine distance indicates greater similarity.

## HNSW

An HNSW index was created using:

`vector_cosine_ops`

HNSW provides approximate nearest-neighbour search and is useful
for larger vector datasets.

## Final Project RAG Flow

Documents → Chunks → Embeddings → pgvector → Similarity Search
→ Retrieved Context → LLM → Answer