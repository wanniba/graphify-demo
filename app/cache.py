"""Redis caching layer for frequently accessed data."""

import json
from typing import Any, List, Optional

from app.config import AppConfig
from app.models import Product, User


class CacheClient:
    """Redis cache wrapper."""

    def __init__(self, config: AppConfig):
        self.config = config.redis
        self._data: dict = {}
        self._ttl = config.redis.ttl

    def get(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set(self, key: str, value: str, ttl: Optional[int] = None):
        self._data[key] = value

    def delete(self, key: str):
        self._data.pop(key, None)

    def flush(self):
        self._data.clear()


class UserCache:
    """Caches user data to reduce database queries."""

    PREFIX = "user:"

    def __init__(self, client: CacheClient):
        self.client = client

    def get_user(self, user_id: int) -> Optional[User]:
        data = self.client.get(f"{self.PREFIX}{user_id}")
        if data:
            d = json.loads(data)
            return User(**d)
        return None

    def set_user(self, user: User):
        key = f"{self.PREFIX}{user.id}"
        self.client.set(key, json.dumps({"id": user.id, "email": user.email, "name": user.name}))

    def invalidate(self, user_id: int):
        self.client.delete(f"{self.PREFIX}{user_id}")


class ProductCache:
    """Caches product listings and individual products."""

    PREFIX = "product:"
    LIST_KEY = "products:available"

    def __init__(self, client: CacheClient):
        self.client = client

    def get_product(self, product_id: int) -> Optional[Product]:
        data = self.client.get(f"{self.PREFIX}{product_id}")
        if data:
            return Product(**json.loads(data))
        return None

    def set_product(self, product: Product):
        key = f"{self.PREFIX}{product.id}"
        self.client.set(key, json.dumps({
            "id": product.id, "name": product.name,
            "price": product.price, "stock": product.stock,
            "vendor_id": product.vendor_id, "category": product.category,
        }))

    def invalidate_product(self, product_id: int):
        self.client.delete(f"{self.PREFIX}{product_id}")
        self.client.delete(self.LIST_KEY)
