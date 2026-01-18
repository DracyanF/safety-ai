import time

def unix_days_ago(days: int) -> int:
    return int(time.time()) - (days * 24 * 60 * 60)

def unix_days_range(start_days_ago: int, end_days_ago: int) -> tuple[int, int]:
    """
    Returns (gte, lt) UNIX timestamps for a time window.
    Example: last 30–60 days
    """
    now = int(time.time())
    gte = now - (end_days_ago * 24 * 60 * 60)
    lt = now - (start_days_ago * 24 * 60 * 60)
    return gte, lt




