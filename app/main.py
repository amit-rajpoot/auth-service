from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.db.database import engine, Base
from app.endpoints.user import router as auth_router
from app.endpoints.auth import router as user_router


# Create FastAPI application
app = FastAPI(
    title="Auth Service"
)

# Create database tables
Base.metadata.create_all(
    bind=engine
)

#Global Exception
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "path":request.url.path,
            "message": "Something went wrong on our end",
            "error": str(exc)
        }
    )

#Routers
app.include_router(
    user_router
)

app.include_router(
    auth_router
)
