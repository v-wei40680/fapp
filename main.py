# example.py
import os
import databases
import ormar
import sqlalchemy
import uvicorn
from fastapi import FastAPI

from fastapi_crudrouter import OrmarCRUDRouter

DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///./test.db")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

app = FastAPI()


def _setup_database():
    # if you do not have the database run this once
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    return engine, database


@app.on_event("startup")
async def startup():
    _setup_database()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Potato(ormar.Model):
    class Meta(BaseMeta):
        pass

    id = ormar.Integer(primary_key=True)
    thickness = ormar.Float()
    mass = ormar.Float()
    color = ormar.String(max_length=255)
    type = ormar.String(max_length=255)


app.include_router(
    OrmarCRUDRouter(
        schema=Potato,
        prefix="potato",
    )
)

if __name__ == "__main__":
    port = os.getenv('PORT', 8000)
    uvicorn.run("main:app", host="127.0.0.1", port=port, log_level="info")

