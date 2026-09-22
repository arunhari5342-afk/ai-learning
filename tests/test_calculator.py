from src.agent_core.tools import calculator


def test_calculator_addition():
    assert calculator("10 + 5") == 15


def test_calculator_multiplication():
    assert calculator("25 * 47") == 1175


def test_calculator_rejects_unsupported_characters():
    try:
        calculator("import os")
        assert False
    except ValueError:
        assert True
