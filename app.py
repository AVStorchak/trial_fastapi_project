import asyncio

from fastapi import FastAPI


from celery_app import celery_main
from sql_app import sql_main
from rabbit_app.pika_client import PikaClient
from rabbit_app.router import router as rabbit_router


class ComplexApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        print('Here we got incoming message %s', message)


app = ComplexApp()


app.include_router(celery_main.router)
app.include_router(rabbit_router)
app.include_router(sql_main.router)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


@app.get("/")
async def root():
    return {"message": "Modular FastAPI application launched!"}
