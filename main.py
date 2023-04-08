from decouple import config

from fastapi import FastAPI, Path, Body, Request, Header, encoders
from motor.motor_asyncio import AsyncIOMotorClient

from models import CarDB

DB_URL = config('DB_URL', cast=str)
DB_NAME = config('DB_NAME', cast=str)

app = FastAPI()

app.mongodb_client = AsyncIOMotorClient(DB_URL)


car = {'brand': 'Fiat', 'make': '500', 'km': 4000, 'cm3': 2000, 'price': 3000, 'year': 1998}
cdb = CarDB(**car)
print(encoders.jsonable_encoder(cdb))


@app.on_event("startup")
async def startup_db_client():
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
