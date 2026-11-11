from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

ProjectName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
# Google Ads customer IDs are 10 digits, optionally written as 123-456-7890.
CustomerId = Annotated[str, Field(pattern=r"^(\d{3}-?\d{3}-?\d{4})?$")]


def _validate_target_url(value: str | None) -> str | None:
    """Allow only empty values or absolute http(s) URLs (no javascript:, file:, etc.)."""
    if value is None:
        return value
    value = value.strip()
    if not value:
        return ""
    if len(value) > 2048:
        raise ValueError("target_url is too long")
    if not value.lower().startswith(("http://", "https://")):
        raise ValueError("target_url must start with http:// or https://")
    return value


class ProjectCreate(BaseModel):
    project_name: ProjectName
    target_url: str = ""
    google_ads_customer_id: CustomerId = ""

    _check_url = field_validator("target_url")(_validate_target_url)


class ProjectUpdate(BaseModel):
    project_name: ProjectName | None = None
    target_url: str | None = None
    google_ads_customer_id: CustomerId | None = None

    _check_url = field_validator("target_url")(_validate_target_url)


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_name: str
    target_url: str
    google_ads_customer_id: str
    created_at: datetime


# Nested schemas for full project load
class AdCopyHeadlineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    position: int
    is_pinned: bool


class AdCopyDescriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    position: int
    is_pinned: bool


class AdCopyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_id: int
    created_at: datetime
    headlines: list[AdCopyHeadlineRead] = []
    descriptions: list[AdCopyDescriptionRead] = []


class KeywordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_id: int
    keyword_text: str
    intent: str
    match_type: str
    status: str


class CampaignRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    campaign_name: str
    budget: float
    bidding_strategy: str
    status: str
    created_at: datetime
    keywords: list[KeywordRead] = []
    ad_copies: list[AdCopyRead] = []


class ProjectWithCampaigns(ProjectRead):
    campaigns: list[CampaignRead] = []
