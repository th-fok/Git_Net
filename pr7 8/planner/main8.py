from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from database.connection8 import init_db, create_db_and_tables
from routes.users8 import user_router
from routes.events8 import event_router
import uvicorn

# Функция для событий жизненного цикла приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске: создаем БД и таблицы
    print("🚀 Starting up...")
    create_db_and_tables()
    yield
    # При выключении
    print("🛑 Shutting down...")

# Создаем приложение с lifespan manager
app = FastAPI(
    title="Planner API with SQL Database",
    description="Event planner with SQLite database",
    version="2.0.0",
    lifespan=lifespan
)

# Корневой маршрут
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Planner API v2.0</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                }
                h1 {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .card {
                    background: rgba(255, 255, 255, 0.2);
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 10px;
                    transition: transform 0.3s;
                }
                .card:hover {
                    transform: translateY(-5px);
                    background: rgba(255, 255, 255, 0.3);
                }
                a {
                    color: white;
                    text-decoration: none;
                    font-weight: bold;
                }
                .endpoint {
                    font-family: monospace;
                    background: rgba(0, 0, 0, 0.3);
                    padding: 5px 10px;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📅 Planner API v2.0</h1>
                <p>Event planner with SQLite database</p>
                
                <div class="card">
                    <h2>📚 Documentation</h2>
                    <p><a href="/docs" target="_blank">Swagger UI Documentation</a></p>
                    <p><a href="/redoc" target="_blank">ReDoc Documentation</a></p>
                </div>
                
                <div class="card">
                    <h2>👤 User Endpoints</h2>
                    <p><span class="endpoint">POST /user/signup</span> - Register new user</p>
                    <p><span class="endpoint">POST /user/signin</span> - User login</p>
                    <p><span class="endpoint">GET /user/</span> - Get all users (admin)</p>
                </div>
                
                <div class="card">
                    <h2>📋 Event Endpoints</h2>
                    <p><span class="endpoint">GET /event/</span> - Get all events</p>
                    <p><span class="endpoint">POST /event/new</span> - Create event</p>
                    <p><span class="endpoint">GET /event/{id}</span> - Get event by ID</p>
                    <p><span class="endpoint">PUT /event/{id}</span> - Update event</p>
                    <p><span class="endpoint">DELETE /event/{id}</span> - Delete event</p>
                </div>
                
                <div class="card">
                    <h2>🛠 Database Info</h2>
                    <p>Database: SQLite (planner.db)</p>
                    <p>ORM: SQLModel (SQLAlchemy + Pydantic)</p>
                </div>
            </div>
        </body>
    </html>
    """

# Регистрация роутеров
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)