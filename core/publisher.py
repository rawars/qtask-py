import redis
import json
from datetime import datetime
from .lua_scripts import LuaScriptLoader

class Publisher:
    def __init__(self, host='localhost', port=6379):
        self.redis = redis.Redis(host=host, port=port)
        self.lua = LuaScriptLoader(self.redis)

    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    def publish(self, queue_name, message_obj, group_name=None):
        timestamp = self.get_timestamp()
        
        # Prepare the keys for Redis
        if group_name:
            counter_key = f"counter:{queue_name}:{group_name}"
            task_prefix = f"task:{queue_name}:{group_name}"
            pending_queue = f"pending:{queue_name}:{group_name}"
            message_obj['group_name'] = group_name
        else:
            counter_key = f"counter:{queue_name}"
            task_prefix = f"task:{queue_name}"
            pending_queue = f"pending:{queue_name}"

        # Prepare the task data
        task_data = {
            'queue': queue_name,
            'group': group_name,
            'status': 'pending',
            'created_at': timestamp,
            'updated_at': timestamp,
            'data': message_obj
        }

        # Execute the Lua script to enqueue the work
        task_id, task_key = self.lua.run(
            'enqueue',
            keys=[counter_key, task_prefix, pending_queue],
            args=[json.dumps(task_data)]
        )
        
        # Update the ID in the data
        task_data['id'] = task_id
        
        print(f"[{timestamp}] Work #{task_id} created in {pending_queue}")
        print(f"Status: {task_data}")
        
        return task_id, task_key

if __name__ == '__main__':
    pub = Publisher()
    pub.publish('WHATSAPP', {"message": "Hello world"}, "batch1")