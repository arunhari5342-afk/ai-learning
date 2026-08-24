CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(4) NOT NULL,
    metadata JSONB
);

CREATE INDEX embeddings_embedding_hnsw_idx
ON embeddings
USING hnsw (embedding vector_cosine_ops);