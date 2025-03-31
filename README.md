# QTask-Py

A Redis-based task queue library for Python, designed for parallel task processing.

## Installation

```bash
pip install qtask-py
```

## Feature

- Parallel task processing
- Multiple workers per group
- Redis-based queuing system
- Task status management
- Detailed logging

## Basic Use

```python
from qtask_py import Publisher, Subscriber

# Configure the publisher
publisher = Publisher(host='localhost', port=6379)

# Post a task
publisher.publish_task(
    queue_name='WHATSAPP',
    group_name='batch1',
    data={'to': '1234567890', 'message': 'Hola mundo'}
)

# Configure the subscriber
def handle_message(data):
    print(f"Processing message: {data}")

subscriber = Subscriber(
    host='localhost',
    port=6379,
    consumers_per_group={'batch1': 3}
)

# Subscribe to a queue
subscriber.subscribe('WHATSAPP', handle_message, 'batch1')
```

## Development

### Environment Configuration

1. Clone the repository:
```bash
git clone https://github.com/rawars/qtask-py.git
cd qtask-py
```

2. Create a virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install in development mode:
```bash
pip install -e .
```

### System Requirements

- Python 3.7 or higher
- Redis Server 5.0 or higher
- Redis Server running on localhost:6379 (or set host/port in the examples)

### Try the Examples

Examples are found in the directory `examples/`:
- `test_publisher.py`: Example of how to publish tasks
- `test_subscriber.py`: Example of how to process tasks with multiple workers

To run the examples, make sure you:

1. Be in the root directory of the project:
```bash
cd /ruta/a/tu/qtask-py
```

2. Have the virtual environment activated:
```bash
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate  # On Windows
```

3. Have Redis Server running:
```bash
# Verify that Redis is running
redis-cli ping
# You should respond with "PONG"
```

4. Run the examples (in separate terminals):
```bash
# Terminal 1 - Start the subscriber
python examples/test_subscriber.py

# Terminal 2 - Run the publisher
python examples/test_publisher.py
```

If you encounter the error "No such file or directory", verify that:
1. You are in the correct directory (use `pwd` to verify)
2. The files exist (use `ls examples/` to verify)
3. The virtual environment is activated (you should see `(venv)` in your prompt)

## Documentation

For more details on usage and configuration, please visit the [full documentation](https://github.com/rawars/qtask-py).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.