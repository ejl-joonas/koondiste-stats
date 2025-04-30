# cache_manager.py
class CacheManager:
    """Manages caching for performance optimization."""
    
    def __init__(self, cache_settings):
        """Initialize with cache settings."""
        self.enabled = cache_settings.get('enabled', True)
        self.storage_type = cache_settings.get('storage', 'memory')
        self.expiration = cache_settings.get('expiration', 3600)  # 1 hour default
        self._initialize_storage()
        
    def _initialize_storage(self):
        """Set up cache storage based on configuration."""
        if self.storage_type == 'memory':
            self.storage = {}
        elif self.storage_type == 'disk':
            self.storage = DiskCache(self.cache_settings.get('path', './cache'))
        elif self.storage_type == 'redis':
            self.storage = RedisCache(self.cache_settings.get('redis_config', {}))
            
    def cache(self, key, data):
        """Store data in cache with the given key."""
        if not self.enabled:
            return
            
        self.storage[key] = {
            'data': data,
            'timestamp': time.time()
        }
        
    def has_cache(self, key):
        """Check if valid cache exists for key."""
        if not self.enabled:
            return False
            
        if key not in self.storage:
            return False
            
        cache_item = self.storage[key]
        if time.time() - cache_item['timestamp'] > self.expiration:
            return False
            
        return True
        
    def get_cache(self, key):
        """Retrieve cache data for key."""
        if not self.enabled or not self.has_cache(key):
            return None
            
        return self.storage[key]['data']
        
    def invalidate(self, key):
        """Invalidate specific cache."""
        if key in self.storage:
            del self.storage[key]