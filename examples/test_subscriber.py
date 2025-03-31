from core.subscriber import Subscriber
import redis


def handle_message(data):
    print(f"Recibido: {data}")


# Configuring consumers by group
consumers_config = {
    "batch1": 3,  # 3 consumers for the batch1 group
    "batch2": 2,  # 2 consumers for the batch2 group
    "batch3": 1  # 3 consumers for the batch3 group
}

# Initialize Redis
redis_client = redis.Redis(host='localhost', port=6379)
sub = Subscriber(
    host="localhost",
    port=6379, 
    consumers_per_group=consumers_config
)

# Subscribe to the batch1 group with 3 consumers
sub.subscribe("WHATSAPP", handle_message, group_name="batch1")

sub.subscribe("WHATSAPP", handle_message, group_name="batch2")

sub.subscribe("WHATSAPP", handle_message, group_name="batch3")

import time

try:
    print("Subscriber started. Waiting for messages...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sub.stop()
