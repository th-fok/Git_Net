from fastapi import APIRouter
from model import Todo

todo_router = APIRouter()
todos = []

@todo_router.post("/todo")
def add_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo added successfully", "todo": todo}

@todo_router.get("/todo")
def get_todos():
    return {"todos": todos}
