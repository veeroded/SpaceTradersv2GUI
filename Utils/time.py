from datetime import datetime, timezone


def istimepassed(timestamp):
    now = datetime.now(timezone.utc)
    if now > datetime.fromisoformat(timestamp.replace("Z", "+00:00")):
        return True
    else:
        return False
