from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Campaign, Project
from app.schemas.project import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    ProjectWithCampaigns,
)

router = APIRouter()


@router.get("/projects", response_model=list[ProjectRead])
def list_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return list(projects)


@router.post("/projects", response_model=ProjectRead)
def create_project(project_in: ProjectCreate, session: Session = Depends(get_session)):
    project = Project(
        project_name=project_in.project_name,
        target_url=project_in.target_url,
        google_ads_customer_id=project_in.google_ads_customer_id or "",
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/projects/{project_id}/full", response_model=ProjectWithCampaigns)
def get_project_full(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    campaigns = session.exec(
        select(Campaign).where(Campaign.project_id == project_id)
    ).all()
    for c in campaigns:
        _ = c.keywords
        _ = c.ad_copies
        for ac in c.ad_copies:
            _ = ac.headlines
            _ = ac.descriptions
    project.campaigns = list(campaigns)
    return project


@router.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    session: Session = Depends(get_session),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    data = project_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return None
