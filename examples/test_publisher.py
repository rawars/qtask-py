from core.publisher import Publisher
import redis

# Initialize Redis
redis_client = redis.Redis(host='localhost', port=6379)

pub = Publisher(host='localhost', port=6379)

# Publish 5 numbered messages
for i in range(1, 6):
    message = {
        "to": "573178181818",
        "message": f"Hello world {i}"
    }
    task_id, task_key = pub.publish('WHATSAPP', message, group_name="batch1")
    print(f"Task #{task_id} created with key {task_key}")


# Publish 7 numbered messages
for i in range(1, 8):
    message = {
        "to": "573178181919",
        "message": f"Hello world {i}"
    }
    task_id, task_key = pub.publish('WHATSAPP', message, group_name="batch2")
    print(f"Task #{task_id} created with key {task_key}")


# Publish 7 numbered messages
for i in range(1, 5):
    message = {
        "to": "573178181009",
        "message": f"Hello world {i}"
    }
    task_id, task_key = pub.publish('WHATSAPP', message, group_name="batch3")
    print(f"Task #{task_id} created with key {task_key}")