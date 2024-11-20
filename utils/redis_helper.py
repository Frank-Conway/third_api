import redis

def get_redis_client():
    return redis.StrictRedis(host='localhost', port=6379, db=0)

def increment_retry_count(url):
    redis_client = get_redis_client()
    key = f"retry_count:{url}"
    count = redis_client.incr(key)
    return count