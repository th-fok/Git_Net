from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from typing import List
from database.connection8 import get_session
from sqlmodel import Session
from models.events8 import Event, EventUpdate

event_router = APIRouter(
    tags=["Events"]
)

# ========== CRUD операции ==========

# CREATE - Создание события
@event_router.post("/new")
async def create_event(new_event: Event, session: Session = Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {
        "message": "Event created successfully",
        "id": new_event.id
    }

# READ ALL - Получение всех событий
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

# READ ONE - Получение события по ID
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {id} does not exist"
        )
    return event

# UPDATE - Обновление события
@event_router.put("/{id}", response_model=Event)
async def update_event(id: int, event_data: EventUpdate, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {id} does not exist"
        )
    
    # Обновляем только переданные поля
    event_data_dict = event_data.dict(exclude_unset=True)
    for key, value in event_data_dict.items():
        setattr(event, key, value)
    
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

# DELETE - Удаление события
@event_router.delete("/{id}")
async def delete_event(id: int, session: Session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {id} does not exist"
        )
    
    session.delete(event)
    session.commit()
    return {"message": "Event deleted successfully"}

# DELETE ALL - Удаление всех событий
@event_router.delete("/")
async def delete_all_events(session: Session = Depends(get_session)) -> dict:
    statement = select(Event)
    events = session.exec(statement).all()
    
    for event in events:
        session.delete(event)
    
    session.commit()
    return {"message": "All events deleted successfully"}