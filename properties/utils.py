from django.core.cache import cache
from .models import Property

def get_all_properties():
    properties = cache.get('all_properties')

    if properties is None:
        print("Cache miss: fetching from database")
        properties = list(Property.objects.all().values())
        cache.set('all_properties', properties, timeout=3600)  # 1 hour
    else:
        print("Cache hit: loaded from Redis")

    return properties
