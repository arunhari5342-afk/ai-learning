from src.agent_core.tools import document_lookup


def test_document_lookup_docuchat():
    result = document_lookup("DocuChat")

    assert "PostgreSQL" in result
    assert "pgvector" in result


def test_document_lookup_rag():
    result = document_lookup("RAG")

    assert "Retrieval-Augmented Generation" in result


def test_document_lookup_unknown_document():
    result = document_lookup("unknown-topic")

    assert result == "No relevant document found."
