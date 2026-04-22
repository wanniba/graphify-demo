"""Email and push notification service."""

from datetime import datetime
from typing import List

from app.config import AppConfig
from app.db import UserRepository
from app.models import Notification, Order, User


class EmailSender:
    """Sends emails via SMTP."""

    def __init__(self, config: AppConfig):
        self.smtp_host = config.notification.smtp_host
        self.smtp_port = config.notification.smtp_port
        self.from_email = config.notification.from_email

    def send(self, to_email: str, subject: str, body: str) -> bool:
        # Simulated email sending
        print(f"Email to {to_email}: {subject}")
        return True


class PushSender:
    """Sends push notifications via API."""

    def __init__(self, config: AppConfig):
        self.api_url = config.notification.push_api_url
        self.api_key = config.notification.push_api_key

    def send(self, user_id: int, title: str, body: str) -> bool:
        # Simulated push notification
        print(f"Push to user {user_id}: {title}")
        return True


class NotificationService:
    """Orchestrates sending notifications across channels."""

    def __init__(self, user_repo: UserRepository, email: EmailSender, push: PushSender):
        self.user_repo = user_repo
        self.email = email
        self.push = push
        self._history: List[Notification] = []
        self._next_id = 1

    def notify_order_confirmed(self, order: Order):
        user = self.user_repo.find_by_id(order.user_id)
        if not user:
            return
        title = f"Order #{order.id} Confirmed"
        body = f"Your order of ${order.total_amount:.2f} has been confirmed."
        self._send(user, title, body)

    def notify_order_shipped(self, order: Order):
        user = self.user_repo.find_by_id(order.user_id)
        if not user:
            return
        title = f"Order #{order.id} Shipped"
        body = f"Your order has been shipped to {order.shipping_address}."
        self._send(user, title, body)

    def notify_order_cancelled(self, order: Order):
        user = self.user_repo.find_by_id(order.user_id)
        if not user:
            return
        title = f"Order #{order.id} Cancelled"
        body = "Your order has been cancelled. A refund will be processed."
        self._send(user, title, body)

    def notify_low_stock(self, product_name: str, vendor: User):
        title = "Low Stock Alert"
        body = f"Product '{product_name}' is running low on stock."
        self._send(vendor, title, body)

    def _send(self, user: User, title: str, body: str):
        self.email.send(user.email, title, body)
        self.push.send(user.id, title, body)
        notification = Notification(
            id=self._next_id,
            user_id=user.id,
            title=title,
            body=body,
            sent_at=datetime.now(),
        )
        self._history.append(notification)
        self._next_id += 1

    def get_user_notifications(self, user_id: int) -> List[Notification]:
        return [n for n in self._history if n.user_id == user_id]
