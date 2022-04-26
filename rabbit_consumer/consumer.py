import pika, sys, os

host = os.environ.get("AMQP_HOST")
queue = os.environ.get("QUEUE_NAME")


def main():
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())

    creds = pika.PlainCredentials("rabbit", "rabbit")
    connection_params = pika.ConnectionParameters(host, 5672, "/", creds, )
    try:
        connection = pika.BlockingConnection(connection_params)
    except Exception as e:
        print(f"Exception occurred: {e}")
        sys.exit(1)
    else:
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        print("Subscribed to " + queue + ", waiting for messages...")
        channel.start_consuming()


if __name__ == "__main__":
    main()
