# test_redis.py

from redis_cache.redis_client import cache_ip, get_cached_ip

ip = "8.8.8.8"
data = {"reputation": "malicious", "source": "AbuseIPDB"}

# Cache it
cache_ip(ip, data)

# Retrieve it
cached = get_cached_ip(ip)
print("Cached IP data:", cached)
