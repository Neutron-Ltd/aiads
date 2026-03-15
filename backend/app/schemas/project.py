from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    project_name: str
    target_url: str = ""
    google_ads_customer_id: str = ""


class ProjectUpdate(BaseModel):
    project_name: str | None = None
    target_url: str | None = None
    google_ads_customer_id: str | None = None


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
