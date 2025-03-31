"""
Lua scripts for atomic operations in Redis.
"""

import os

def get_script_content(script_name):
    """Read the content of a Lua script from the directory."""
    script_path = os.path.join(os.path.dirname(__file__), f"{script_name}.lua")
    with open(script_path, "r") as f:
        return f.read()

# Load scripts
ENQUEUE_SCRIPT = get_script_content("enqueue")
DEQUEUE_SCRIPT = get_script_content("dequeue")
GET_STATUS_SCRIPT = get_script_content("get_status")
UPDATE_STATUS_SCRIPT = get_script_content("update_status")

__all__ = [
    'ENQUEUE_SCRIPT',
    'DEQUEUE_SCRIPT',
    'GET_STATUS_SCRIPT',
    'UPDATE_STATUS_SCRIPT'
] 