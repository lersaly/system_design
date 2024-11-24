import json
import redis
from sqlalchemy.future import select
from models import Conference

class RedisCacheService:
    def __init__(self, redis_url="redis://redis:6379/0"):
        self.redis_client = redis.from_url(redis_url)
        self.CACHE_PREFIX = "conference:"

    def get_conference_with_cache(self, db, conference_id):
        # Check cache first (through reading)
        cached_conference = self.redis_client.get(f"{self.CACHE_PREFIX}{conference_id}")
        
        if cached_conference:
            return json.loads(cached_conference)
        
        # If not in cache, fetch from database
        conference = db.get(Conference, conference_id)
        
        if conference:
            # Store in cache
            self.redis_client.setex(
                f"{self.CACHE_PREFIX}{conference_id}", 
                3600,  # 1 hour expiration 
                json.dumps({
                    "id": conference.id,
                    "title": conference.title
                })
            )
            return conference
        
        return None

    def invalidate_conference_cache(self, conference_id):
        self.redis_client.delete(f"{self.CACHE_PREFIX}{conference_id}")