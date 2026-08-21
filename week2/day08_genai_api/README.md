# Day 8 - GenAI Meets Backend + SQL Revamp

## Overview

A FastAPI backend that connects an LLM with PostgreSQL for
conversation persistence.

## Features

- LLM integration
- FastAPI `/generate` endpoint
- PostgreSQL persistence
- Conversation storage
- Message storage
- JSONB metadata
- Conversation history endpoint
- Swagger API testing

## Endpoints

### Generate

POST `/generate`

Example request:

```json
{
    "conversation_id": "11111111-1111-1111-1111-111111111111",
    "prompt": "Explain embeddings in simple words."
}