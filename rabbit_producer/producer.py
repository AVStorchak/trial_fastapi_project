import os
import pika

from fastapi import APIRouter

router = APIRouter(prefix="/rabbit", tags=["rabbit producer"])
# host = os.environ.get("AMQP_HOST")
# queue = os.environ.get("QUEUE_NAME")
host = "rabbitmq"
queue = "hello"


@router.post("/publish-message/")
def publish_message(message: str):
    creds = pika.PlainCredentials("rabbit", "rabbit")
    connection_params = pika.ConnectionParameters(host, 5672, "/", creds, )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="",
                          routing_key=queue,
                          body=bytes(message, "utf-8"))
    print(f" [x] Sent {message}")
    connection.close()
    return {"info": "message sent successfully"}
