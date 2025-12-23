from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes.users8 import user_router
from routes.events8 import event_router
import uvicorn

app = FastAPI()

# Корневой маршрут
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Planner API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; }
                a { color: #0066cc; text-decoration: none; }
                a:hover { text-decoration: underline; }
                ul { list-style-type: none; padding: 0; }
                li { margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>📅 Planner Event API</h1>
            <p>API для управления событиями и пользователями</p>
            <ul>
                <li><a href="/docs" target="_blank">📚 Документация API (Swagger)</a></li>
                <li><a href="/redoc" target="_blank">📖 Альтернативная документация (ReDoc)</a></li>
                <li><a href="/user/signup">👤 Регистрация пользователя</a></li>
                <li><a href="/event/">📋 Все события</a></li>
            </ul>
        </body>
    </html>
    """

# Регистрация роутеров
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)