import time
from typing import Any

def get_time(_: Any = None) -> str:
    """Return current timestamp."""
    return time.strftime("%Y-%m-%d %H:%M:%S")

TOOLS = {
    "get_time": {"fn": get_time, "desc": "Return current timestamp"},
}
