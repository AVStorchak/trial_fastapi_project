import os
import pika

from fastapi import APIRouter

router = APIRouter(prefix="/rabbit", tags=["rabbit producer"])
# host = os.environ.get("AMQP_HOST")
# queue = os.environ.get("QUEUE_NAME")
host = "localhost"
queue = "hello"


@router.post("/publish-message/")
def publish_message(message: str):
    connection_params = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="",
                          routing_key="hello",
                          body=message)
    print(f" [x] Sent {message}")
    connection.close()
    return {"info": "message sent successfully"}
