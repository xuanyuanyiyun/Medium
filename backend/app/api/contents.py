from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Content, ContentType, ContentStatus
from app.schemas import ContentCreate, ContentUpdate, ContentResponse

router = APIRouter(prefix="/contents", tags=["contents"])


@router.post("/", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    db: AsyncSession = Depends(get_db),
):
    content = Content(
        project_id=content_data.project_id,
        type=ContentType(content_data.type.value),
        title=content_data.title,
        body=content_data.body,
        outline=content_data.outline,
        status=ContentStatus.DRAFT,
    )
    
    db.add(content)
    await db.commit()
    await db.refresh(content)
    
    return content


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content


@router.patch("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_data: ContentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    update_data = content_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(content, key, value)
    
    await db.commit()
    await db.refresh(content)
    
    return content


@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    await db.delete(content)
    await db.commit()
    
    return {"message": "Content deleted successfully"}
