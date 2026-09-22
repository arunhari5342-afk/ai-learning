import pytest

from src.agent_core.tools import mock_db_query


def test_mock_db_users():
    result = mock_db_query("users")

    assert len(result) == 2
    assert result[0]["name"] == "Arun"


def test_mock_db_limit():
    result = mock_db_query("users", limit=1)

    assert len(result) == 1


def test_mock_db_unknown_table():
    with pytest.raises(ValueError):
        mock_db_query("passwords")
