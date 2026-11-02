import shutil


def classify(usage_percent):
    """Turn a disk usage percentage into a status."""
    if usage_percent < 0 or usage_percent > 100:
        raise ValueError("usage must be between 0 and 100")
    if usage_percent >= 90:
        return "CRITICAL"
    if usage_percent >= 75:
        return "WARNING"
    return "OK"


def disk_usage_percent(path="/"):
    """Return how full a filesystem is, in percent."""
    total, used, free = shutil.disk_usage(path)
    return round(used / total * 100, 1)


if __name__ == "__main__":
    percent = disk_usage_percent("/")
    print(f"Disk usage on /: {percent}% -> {classify(percent)}")
