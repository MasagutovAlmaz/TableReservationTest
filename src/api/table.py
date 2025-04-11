from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.models.table import Table
from src.schemas.table import ResponseTable, RequestTable

router = APIRouter(tags=["Table"], prefix="/api/table")

@router.post("/table", response_model=ResponseTable)
async def create_table(table: RequestTable, db: AsyncSession = Depends(get_db)):

    new_table = Table(
        name=table.name,
        seats=table.seats,
        location=table.location
    )

    db.add(new_table)
    try:
        await db.commit()
        await db.refresh(new_table)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании мероприятия: {str(e)}"
        )
    return ResponseTable(**new_table.__dict__)

@router.get("/table/all", response_model=list[ResponseTable])
async def get_all_tables(db: AsyncSession = Depends(get_db)):
    tables = await db.execute(select(Table))
    return [ResponseTable(**table.__dict__) for table in tables.scalars().all()]

@router.delete("/table/{table_id}")
async def delete_table(table_id: int, db: AsyncSession = Depends(get_db)):
    table = await db.execute(select(Table).where(Table.id == table_id))
    table = table.scalar_one_or_none()
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Стол не найден")

    await db.delete(table)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении Столика: {str(e)}"
        )
    return {"Сообщение": "Столик был удален успешно"}