"""
Pydantic schemas for server-side tool input validation.
Enforces typed fields, required parameters, and extra="forbid" (additionalProperties: false).
"""
from pydantic import BaseModel, Field, ConfigDict


class BaseToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SearchKnowledgeBaseInput(BaseToolInput):
    query: str = Field(..., min_length=1, description="Keywords to search within notes/records")
    campaign_id: int = Field(..., ge=1, description="Target campaign ID to scope search")
    top_k: int = Field(default=3, ge=1, le=10, description="Max number of search results to return")


class UpdateCampaignBudgetInput(BaseToolInput):
    campaign_id: int = Field(..., ge=1, description="Campaign ID to update")
    new_budget: float = Field(..., gt=0.0, description="New budget amount (must be positive)")


class PauseCampaignInput(BaseToolInput):
    campaign_id: int = Field(..., ge=1, description="ID of campaign to pause")
    reason: str = Field(..., min_length=10, description="Detailed explanation for pausing campaign")