import time

RATE_LIMIT_SEC = 3
_last_request: dict[int, float] = {}


def check_rate_limit(user_id: int) -> bool:
    """Returns True if request is allowed."""
    now = time.time()
    if now - _last_request.get(user_id, 0) < RATE_LIMIT_SEC:
        return False
    _last_request[user_id] = now
    return True
