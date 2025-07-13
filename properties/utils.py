from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

def get_all_properties():
    properties = cache.get('all_properties')

    if properties is None:
        print("Cache miss: fetching from database")
        properties = list(Property.objects.all().values())
        cache.set('all_properties', properties, timeout=3600)  # 1 hour
    else:
        print("Cache hit: loaded from Redis")

    return properties

def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    print(f"Redis Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {metrics['hit_ratio']}")
    return metrics