import os


def getenv(key):
    return os.getenv(key, "").strip()
