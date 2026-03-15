"""
All models in one file to avoid circular import issues with SQLAlchemy Relationship.
"""
from datetime import datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class Project(SQLModel, table=True):
    __tablename__ = "project"

    id: int | None = Field(default=None, primary_key=True)
    project_name: str = Field(index=True)
    target_url: str = ""
    google_ads_customer_id: str = ""  # Google Ads account ID (e.g. 123-456-7890)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    campaigns: list["Campaign"] = Relationship(back_populates="project")


class CampaignStatus(str, Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    ACTIVE = "Active"


class Campaign(SQLModel, table=True):
    __tablename__ = "campaign"

    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    campaign_name: str = Field(index=True)
    budget: float = 0.0
    bidding_strategy: str = ""
    status: str = Field(default=CampaignStatus.DRAFT.value)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    project: Project | None = Relationship(back_populates="campaigns")
    keywords: list["Keyword"] = Relationship(back_populates="campaign")
    ad_copies: list["AdCopy"] = Relationship(back_populates="campaign")


class KeywordStatus(str, Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    NEGATIVE = "Negative"


class Keyword(SQLModel, table=True):
    __tablename__ = "keyword"

    id: int | None = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id", index=True)
    keyword_text: str = Field(index=True)
    intent: str = ""
    match_type: str = ""
    status: str = Field(default=KeywordStatus.APPROVED.value)

    campaign: Campaign | None = Relationship(back_populates="keywords")


class AdCopy(SQLModel, table=True):
    __tablename__ = "ad_copy"

    id: int | None = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    campaign: Campaign | None = Relationship(back_populates="ad_copies")
    headlines: list["AdCopyHeadline"] = Relationship(back_populates="ad_copy")
    descriptions: list["AdCopyDescription"] = Relationship(back_populates="ad_copy")


class AdCopyHeadline(SQLModel, table=True):
    __tablename__ = "ad_copy_headline"

    id: int | None = Field(default=None, primary_key=True)
    ad_copy_id: int = Field(foreign_key="ad_copy.id", index=True)
    text: str = ""
    position: int = 0
    is_pinned: bool = False

    ad_copy: AdCopy | None = Relationship(back_populates="headlines")


class AdCopyDescription(SQLModel, table=True):
    __tablename__ = "ad_copy_description"

    id: int | None = Field(default=None, primary_key=True)
    ad_copy_id: int = Field(foreign_key="ad_copy.id", index=True)
    text: str = ""
    position: int = 0
    is_pinned: bool = False

    ad_copy: AdCopy | None = Relationship(back_populates="descriptions")
