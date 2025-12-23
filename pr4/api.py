from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from todo import todo_router

app = FastAPI()

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(todo_router)
