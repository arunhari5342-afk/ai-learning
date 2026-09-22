"""
Pydantic schemas used to validate agent tool arguments.
"""

from pydantic import BaseModel, Field


class CalculatorArgs(BaseModel):
    """Arguments required by the calculator tool."""

    expression: str = Field(
        ...,
        description="Mathematical expression to calculate",
    )


class DocumentLookupArgs(BaseModel):
    """Arguments required by the document lookup tool."""

    query: str = Field(
        ...,
        min_length=1,
        description="Search query for the document store",
    )


class MockDBArgs(BaseModel):
    """Arguments required by the mock database query tool."""

    table: str = Field(
        ...,
        description="Table to query",
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of rows to return",
    )
