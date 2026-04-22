"""Data models for the application."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    VENDOR = "vendor"


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class User:
    id: int
    email: str
    name: str
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def can_manage_orders(self) -> bool:
        return self.role in (UserRole.ADMIN, UserRole.VENDOR)


@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int
    vendor_id: int
    category: str = ""
    description: str = ""

    def is_available(self) -> bool:
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> bool:
        if quantity > self.stock:
            return False
        self.stock -= quantity
        return True


@dataclass
class OrderItem:
    product_id: int
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    id: int
    user_id: int
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    shipping_address: str = ""

    @property
    def total_amount(self) -> float:
        return sum(item.total for item in self.items)

    def confirm(self) -> bool:
        if self.status != OrderStatus.PENDING:
            return False
        self.status = OrderStatus.CONFIRMED
        return True

    def cancel(self) -> bool:
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            return False
        self.status = OrderStatus.CANCELLED
        return True


@dataclass
class Notification:
    id: int
    user_id: int
    title: str
    body: str
    channel: str = "email"
    sent_at: Optional[datetime] = None
    read: bool = False
