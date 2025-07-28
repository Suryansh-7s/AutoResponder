# redis_cache/redis_client.py

import redis
import json
import os
from dotenv import load_dotenv
load_dotenv()

r = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

def cache_ip(ip_address, metadata, ttl_seconds=3600):
    """Store enriched IP metadata in Redis"""
    r.setex(ip_address, ttl_seconds, json.dumps(metadata))

def get_cached_ip(ip_address):
    """Retrieve IP metadata from Redis if exists"""
    result = r.get(ip_address)
    if result:
        return json.loads(result)
    return None

def incr_failed_attempt(ip_address, threshold=3600):
    """Increment failed attempt count for an IP. Returns the new count."""
    key = f"failcount:{ip_address}"
    count = r.incr(key)
    r.expire(key, threshold)
    return count

def reset_failed_attempts(ip_address):
    """Reset failed attempt count for an IP."""
    key = f"failcount:{ip_address}"
    r.delete(key)
