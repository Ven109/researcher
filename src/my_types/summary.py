from pydantic import BaseModel, Field


# Pydantic
class Summary(BaseModel):
    """Summary of articles"""

    summary: str = Field(description="The summary of the article")

    skipped: bool = Field(
        description="Whether the article was skipped, if the article is not relevant",
    )
