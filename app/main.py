from fastapi import FastAPI

from app.interfaces.rest.api import api_router
from app.infra import database

app = FastAPI()


# app startup handler
@app.on_event("startup")
async def startup_event():
    database.connect()


# app shutdown handler
@app.on_event("shutdown")
async def shutdown_event():
    database.disconnect()


# set app router
app.include_router(api_router)
