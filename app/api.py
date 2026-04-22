"""REST API endpoints - the main entry point tying all modules together."""

from typing import Dict, List, Optional

from app.auth import AuthService, check_permission
from app.cache import CacheClient, ProductCache, UserCache
from app.config import AppConfig, load_config
from app.db import (
    DatabaseConnection,
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from app.models import Order, OrderItem, OrderStatus, Product, User
from app.notifications import EmailSender, NotificationService, PushSender


class APIServer:
    """Main API server that wires all components together."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or load_config()

        # Infrastructure
        self.db = DatabaseConnection(self.config)
        self.cache = CacheClient(self.config)

        # Repositories
        self.users = UserRepository(self.db)
        self.products = ProductRepository(self.db)
        self.orders = OrderRepository(self.db)

        # Caches
        self.user_cache = UserCache(self.cache)
        self.product_cache = ProductCache(self.cache)

        # Services
        from app.auth import TokenManager
        self.auth = AuthService(
            self.users, self.user_cache,
            TokenManager(self.config.secret_key),
        )
        self.notifications = NotificationService(
            self.users,
            EmailSender(self.config),
            PushSender(self.config),
        )

    def startup(self):
        self.db.connect()

    def shutdown(self):
        self.db.disconnect()
        self.cache.flush()

    # --- Auth endpoints ---

    def login(self, email: str, password: str) -> Dict:
        token = self.auth.authenticate(email, password)
        if not token:
            return {"error": "Invalid credentials", "status": 401}
        return {"token": token, "status": 200}

    def logout(self, token: str) -> Dict:
        self.auth.logout(token)
        return {"message": "Logged out", "status": 200}

    # --- Product endpoints ---

    def list_products(self, category: Optional[str] = None) -> List[Dict]:
        products = self.products.find_available(category)
        return [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]

    def get_product(self, product_id: int) -> Dict:
        product = self.product_cache.get_product(product_id)
        if not product:
            product = self.products.find_by_id(product_id)
            if product:
                self.product_cache.set_product(product)
        if not product:
            return {"error": "Product not found", "status": 404}
        return {"id": product.id, "name": product.name, "price": product.price, "stock": product.stock}

    # --- Order endpoints ---

    def create_order(self, token: str, items: List[Dict], shipping_address: str) -> Dict:
        user = self.auth.get_current_user(token)
        if not user:
            return {"error": "Unauthorized", "status": 401}

        order_items = []
        for item in items:
            product = self.products.find_by_id(item["product_id"])
            if not product or not product.reduce_stock(item["quantity"]):
                return {"error": f"Product {item['product_id']} unavailable", "status": 400}
            order_items.append(OrderItem(
                product_id=product.id,
                quantity=item["quantity"],
                unit_price=product.price,
            ))
            self.products.save(product)
            self.product_cache.invalidate_product(product.id)

        order = Order(
            id=len(self.orders._store) + 1,
            user_id=user.id,
            items=order_items,
            shipping_address=shipping_address,
        )
        self.orders.save(order)
        return {"order_id": order.id, "total": order.total_amount, "status": 201}

    def confirm_order(self, token: str, order_id: int) -> Dict:
        user = self.auth.get_current_user(token)
        if not user:
            return {"error": "Unauthorized", "status": 401}

        order = self.orders.find_by_id(order_id)
        if not order:
            return {"error": "Order not found", "status": 404}

        if not check_permission(user, order.user_id):
            return {"error": "Forbidden", "status": 403}

        if not order.confirm():
            return {"error": "Cannot confirm order", "status": 400}

        self.orders.save(order)
        self.notifications.notify_order_confirmed(order)
        return {"message": "Order confirmed", "status": 200}

    def cancel_order(self, token: str, order_id: int) -> Dict:
        user = self.auth.get_current_user(token)
        if not user:
            return {"error": "Unauthorized", "status": 401}

        order = self.orders.find_by_id(order_id)
        if not order:
            return {"error": "Order not found", "status": 404}

        if not check_permission(user, order.user_id):
            return {"error": "Forbidden", "status": 403}

        if not order.cancel():
            return {"error": "Cannot cancel order", "status": 400}

        self.orders.save(order)
        self.notifications.notify_order_cancelled(order)
        return {"message": "Order cancelled", "status": 200}

    def get_user_orders(self, token: str) -> List[Dict]:
        user = self.auth.get_current_user(token)
        if not user:
            return [{"error": "Unauthorized", "status": 401}]

        orders = self.orders.find_by_user(user.id)
        return [
            {"id": o.id, "total": o.total_amount, "status": o.status.value, "items": len(o.items)}
            for o in orders
        ]

    # --- Notification endpoints ---

    def get_notifications(self, token: str) -> List[Dict]:
        user = self.auth.get_current_user(token)
        if not user:
            return [{"error": "Unauthorized", "status": 401}]

        notifications = self.notifications.get_user_notifications(user.id)
        return [{"id": n.id, "title": n.title, "body": n.body, "read": n.read} for n in notifications]
