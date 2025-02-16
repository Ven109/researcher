from pydantic import BaseModel, Field


class KeyPoint(BaseModel):
    """Key point"""

    value: str = Field(description="Key point content")
    source: str = Field(description="Source of the information")
    source_link: str = Field(description="Link of the source")


class ResearchCluster(BaseModel):
    """Research result cluster"""

    cluster_title: str = Field(description="Title of the cluster")
    key_points: list[KeyPoint] = Field(
        description="List of key points for the cluster",
    )


class ResearchResult(BaseModel):
    """Research result"""

    clusters: list[ResearchCluster] = Field(
        description="List of clusters with key points"
    )
