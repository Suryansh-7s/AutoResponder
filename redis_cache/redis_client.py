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
