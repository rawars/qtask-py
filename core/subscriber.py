import redis
import json
import threading
import time
from datetime import datetime


class Subscriber:
    def __init__(self, host="localhost", port=6379, consumers_per_group=None):
        self.redis = redis.Redis(host=host, port=port)
        self.running = True
        self.consumers_per_group = consumers_per_group or {}
        self.workers = []
        self.print_lock = threading.Lock()  # To synchronize the output

    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    def notify_task_completed(self):
        time.sleep(0.1)
        self.redis.publish("next_task_ready", "ready")

    def acquire_worker_lock(self, worker_id):
        lock_key = f"worker_lock:{worker_id}"
        return self.redis.set(lock_key, "1", nx=True, ex=5)

    def release_worker_lock(self, worker_id):
        lock_key = f"worker_lock:{worker_id}"
        self.redis.delete(lock_key)

    def get_task_id_from_key(self, task_key):
        return task_key.split(":")[-1]

    def update_task_status(self, task_key, status, worker_id, error=None):
        raw_data = self.redis.hget(task_key, 'data')
        if not raw_data:
            raise Exception(f"Job with key not found {task_key}")
            
        task_data = json.loads(raw_data)
        task_data['status'] = status
        task_data['updated_at'] = self.get_timestamp()
        task_data['worker_id'] = worker_id
        
        if error:
            task_data['error'] = str(error)
        
        self.redis.hset(task_key, 'data', json.dumps(task_data))
        return task_data

    def print_log(self, *messages, worker_id=None, task_id=None):
        # Use a lock to avoid mixing messages
        with self.print_lock:
            print("="*50)
            timestamp = self.get_timestamp()
            prefix = f"[{timestamp}]"
            if worker_id:
                prefix += f" [{worker_id}]"
            if task_id:
                prefix += f" [Job #{task_id}]"
            
            for message in messages:
                if isinstance(message, dict):
                    for key, value in message.items():
                        print(f"{key:<10}: {value}")
                else:
                    print(f"{prefix} {message}")
            print("="*50 + "\n")

    def subscribe(self, queue_name, callback, group_name=None):
        if group_name:
            queue_key = f"{queue_name}:{group_name}"
            num_consumers = self.consumers_per_group.get(group_name, 1)
        else:
            queue_key = queue_name
            num_consumers = 1

        def process_task(task_key, queue, worker_id):
            try:
                task_id = self.get_task_id_from_key(task_key)
                
                # Get the job data
                raw_data = self.redis.hget(task_key, 'data')
                if not raw_data:
                    raise Exception(f"Job with key not found {task_key}")
                    
                task_data = json.loads(raw_data)

                # Update status to "processing"
                task_data = self.update_task_status(task_key, 'processing', worker_id)
                
                start_time = self.get_timestamp()
                
                self.print_log(
                    "START PROCESSING",
                    {
                        "Queue": queue,
                        "Group": task_data['group'],
                        "Created": task_data['created_at'],
                        "Started": start_time,
                        "Message": task_data['data'].get('message', 'N/A'),
                        "To": task_data['data'].get('to', 'N/A')
                    },
                    worker_id=worker_id,
                    task_id=task_id
                )

                # Process the job
                time.sleep(2)  # Simulate processing
                callback(task_data['data'])

                # Update status to "completed"
                task_data = self.update_task_status(task_key, 'completed', worker_id)
                
                end_time = self.get_timestamp()
                self.print_log(
                    "FINISHED PROCESSING",
                    {
                        "Duration": f"{(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')).total_seconds():.3f}s",
                        "Status": "Completed",
                        "Finished": end_time,
                        "Message": task_data['data'].get('message', 'N/A')
                    },
                    worker_id=worker_id,
                    task_id=task_id
                )

            except Exception as e:
                self.print_log(
                    "ERROR IN PROCESSING",
                    {
                        "Error": str(e),
                        "Status": "Failed",
                        "Message": task_data['data'].get('message', 'N/A') if 'task_data' in locals() else 'N/A'
                    },
                    worker_id=worker_id,
                    task_id=task_id
                )
                if 'task_key' in locals():
                    self.update_task_status(task_key, 'failed', worker_id, error=str(e))

        def worker_loop(worker_num):
            worker_id = f"Worker-{worker_num}"
            pending_queue = f"pending:{queue_key}"
            
            self.print_log(
                f"Started and listening to queue: {pending_queue}",
                worker_id=worker_id
            )

            while self.running:
                try:
                    # Try to get a job using BLPOP with timeout
                    result = self.redis.blpop(pending_queue, timeout=1)
                    
                    if result:
                        _, task_key = result
                        task_key = task_key.decode()
                        process_task(task_key, queue_key, worker_id)

                except Exception as e:
                    self.print_log(
                        f"Connection error: {e}",
                        worker_id=worker_id
                    )
                    time.sleep(1)

        # Create the workers according to the configuration
        for i in range(num_consumers):
            thread = threading.Thread(target=worker_loop, args=(i+1,))
            thread.daemon = True
            self.workers.append(thread)
            thread.start()

    def stop(self):
        self.print_log("Stopping workers...")
        self.running = False
        time.sleep(0.1)  # Small pause to ensure workers finish
        self.print_log("Workers stopped")


if __name__ == "__main__":
    def handle_message(data):
        print(f"Received: {data}")

    # Example of consumer configuration by group
    consumers_config = {
        "batch1": 3,  # 3 consumers for the batch1 group
        "batch2": 2   # 2 consumers for the batch2 group
    }

    subscriber = Subscriber(
        host="localhost", 
        port=6379, 
        consumers_per_group=consumers_config
    )
    
    # Subscribe to different groups
    subscriber.subscribe("WHATSAPP", handle_message, "batch1")
    subscriber.subscribe("WHATSAPP", handle_message, "batch2")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        subscriber.stop()
