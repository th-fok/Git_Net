from fastapi import APIRouter, Body, HTTPException, status
from models.events8 import Event
from typing import List

event_router = APIRouter(
    tags=["Events"]
)

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found"
    )

@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    events.append(body)
    return {"message": "Event created successfully"}

@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found"
    )

@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "All events deleted"}

@event_router.put("/{id}")
async def update_event(id: int, body: Event = Body(...)) -> dict:
    for index, event in enumerate(events):
        if event.id == id:
            # Создаем словарь текущего события
            event_dict = event.dict()
            # Обновляем его данными из body
            update_data = body.dict(exclude_unset=True)
            updated_event = event_dict.copy()
            updated_event.update(update_data)
            # Заменяем событие в списке
            events[index] = Event(**updated_event)
            return {"message": "Event updated successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )