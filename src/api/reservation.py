from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime
from src.db.database import get_db
from src.models.reservation import Reservation
from src.schemas.reservation import ResponseReservation, RequestReservation

router = APIRouter(tags=["reservation"], prefix="/api/reservation")

@router.post("/reservation", response_model=ResponseReservation)
async def create_reservation(reservation: RequestReservation, db: AsyncSession = Depends(get_db)):
    duration_minutes = float(reservation.duration_time) if isinstance(reservation.duration_time,
                                                                      Decimal) else reservation.duration_time

    # Validate duration is positive
    if duration_minutes <= 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бронирование должно быть больше или равняться 30 минутам"
        )

    reservation_end_time = reservation.reservation_time + timedelta(minutes=duration_minutes)

    existing = await db.execute(
        select(Reservation)
        .where(Reservation.table_id == reservation.table_id)
    )
    existing_reservations = existing.scalars().all()

    for existing_res in existing_reservations:
        existing_duration = float(existing_res.duration_time)
        existing_end = existing_res.reservation_time + timedelta(minutes=existing_duration)

        if (reservation.reservation_time < existing_end and
                reservation_end_time > existing_res.reservation_time):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Столик уже забронирован с {existing_res.reservation_time} до {existing_end}"
            )

    new_reservation = Reservation(
        customer_name=reservation.customer_name,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_time=reservation.duration_time
    )

    db.add(new_reservation)
    try:
        await db.commit()
        await db.refresh(new_reservation)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании резервации: {str(e)}"
        )

    return ResponseReservation(**new_reservation.__dict__)

@router.get("/reservation/all", response_model=list[ResponseReservation])
async def get_all_reservations(db: AsyncSession = Depends(get_db)):
    reservations = await db.execute(select(Reservation))
    return [ResponseReservation(**reservation.__dict__) for reservation in reservations.scalars().all()]


@router.delete("/reservation/{reservation_id}", response_model=ResponseReservation)
async def delete_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    reservation = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = reservation.scalar_one_or_none()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Резервация не найдена")

    await db.delete(reservation)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении резервации: {str(e)}"
        )
    return ResponseReservation(**reservation.__dict__)

