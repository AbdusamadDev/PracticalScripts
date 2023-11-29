from datetime import datetime, timedelta
from typing import Dict, Any


class CacheManager(object):
    def __str__(self):
        return """
        Base Cache Manager.\n
        Manages the cache system\n
        Methods: is_expired, size_exceeded, get_oldest_cache, get, set, data
        """

    def __init__(self, data: Dict, size: int):
        self.__data = data
        self.size = size
        super().__init__()

    @property
    def data(self):
        """Cache data is meant to be Read Only type of data."""
        return self.__data

    def get_oldest_cache(self):
        """Returns the oldest added cache"""
        cache_expirations = [self.data.get(key).get("exp") for key in self.data]
        filter_set = {
            self.data.get(key).get("exp"): key for key in self.data
        }
        return filter_set.get(min(cache_expirations))

    @property
    def size_exceeded(self):
        return self.size <= len(self.data)

    def get(self, key: Any):
        """Returns cache based on key"""
        result = self.data.get(key, None)
        if result is None:
            return {}
        return {key: result}

    def set(self, key: Any, value: Any, exp: datetime):
        """Sets cache data to Cache Manager"""
        if self.size_exceeded:
            del self.data[self.get_oldest_cache()]
        self.data[key] = {"value": value, "exp": exp}


if __name__ == '__main__':
    a = {
        "qqqqqqqqq": {"value": "data1", "exp": datetime.now() - timedelta(days=1)},
        "keysad1": {"value": "data1", "exp": datetime.now()},
        "key2": {"value": "data2", "exp": datetime.now() + timedelta(minutes=10)}
    }
    cache_manager = CacheManager(data=a, size=2)
    cache_manager.set("salom", "asdfhjklahsdfhlaskdf", datetime.now() + timedelta(hours=24))
    print(cache_manager.data)
    print(cache_manager.get("salom"))
