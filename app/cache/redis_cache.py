try:
    import redis
    client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    client.ping()
    USE_REDIS = True
except Exception:
    client = None
    USE_REDIS = False

import json

cache = {}  # fallback in-memory


def get_cache(key):
    if USE_REDIS:
        try:
            val = client.get(key)
            return json.loads(val) if val else None
        except Exception:
            pass
    return cache.get(key)


def set_cache(key, value, ttl=300):
    if USE_REDIS:
        try:
            client.setex(key, ttl, json.dumps(value, default=str))
            return
        except Exception:
            pass
    cache[key] = value


def clear_cache(key):
    if USE_REDIS:
        try:
            client.delete(key)
        except Exception:
            pass
    cache.pop(key, None)