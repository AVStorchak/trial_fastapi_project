"""A standalone file for testing RabbitMQ functionality"""

import pika
import sys
import os

host = os.getenv('AMQP_HOST')
queue = os.getenv('QUEUE_NAME')

print(host)

# def main():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
#     channel = connection.channel()
#
#     channel.queue_declare(queue=queue)
#
#     def callback(ch, method, properties, body):
#         print(" [x] Received %r" % body)
#
#     channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
#
#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()
#
#
# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
