"""Database connection and query layer."""

from typing import Dict, List, Optional

from app.config import AppConfig, load_config
from app.models import Order, OrderItem, OrderStatus, Product, User, UserRole


class DatabaseConnection:
    """Manages database connection pool."""

    def __init__(self, config: AppConfig):
        self.config = config.database
        self._pool = None

    def connect(self):
        """Establish connection pool."""
        self._pool = {
            "host": self.config.host,
            "port": self.config.port,
            "dbname": self.config.name,
            "pool_size": self.config.pool_size,
        }

    def disconnect(self):
        """Close all connections."""
        self._pool = None

    @property
    def is_connected(self) -> bool:
        return self._pool is not None


class UserRepository:
    """Data access for User entities."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self._store: Dict[int, User] = {}

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._store.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._store.values():
            if user.email == email:
                return user
        return None

    def save(self, user: User) -> User:
        self._store[user.id] = user
        return user

    def list_active(self) -> List[User]:
        return [u for u in self._store.values() if u.is_active]


class ProductRepository:
    """Data access for Product entities."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self._store: Dict[int, Product] = {}

    def find_by_id(self, product_id: int) -> Optional[Product]:
        return self._store.get(product_id)

    def find_by_vendor(self, vendor_id: int) -> List[Product]:
        return [p for p in self._store.values() if p.vendor_id == vendor_id]

    def find_available(self, category: Optional[str] = None) -> List[Product]:
        products = [p for p in self._store.values() if p.is_available()]
        if category:
            products = [p for p in products if p.category == category]
        return products

    def save(self, product: Product) -> Product:
        self._store[product.id] = product
        return product


class OrderRepository:
    """Data access for Order entities."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self._store: Dict[int, Order] = {}

    def find_by_id(self, order_id: int) -> Optional[Order]:
        return self._store.get(order_id)

    def find_by_user(self, user_id: int) -> List[Order]:
        return [o for o in self._store.values() if o.user_id == user_id]

    def find_by_status(self, status: OrderStatus) -> List[Order]:
        return [o for o in self._store.values() if o.status == status]

    def save(self, order: Order) -> Order:
        self._store[order.id] = order
        return order
