"""Authentication and authorization module."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple

from app.cache import UserCache
from app.db import UserRepository
from app.models import User, UserRole


class PasswordHasher:
    """Handles password hashing and verification."""

    @staticmethod
    def hash(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        if salt is None:
            salt = secrets.token_hex(16)
        hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        return hashed, salt

    @staticmethod
    def verify(password: str, hashed: str, salt: str) -> bool:
        check, _ = PasswordHasher.hash(password, salt)
        return check == hashed


class TokenManager:
    """Manages authentication tokens."""

    def __init__(self, secret_key: str, ttl_hours: int = 24):
        self.secret_key = secret_key
        self.ttl_hours = ttl_hours
        self._tokens: dict = {}

    def create_token(self, user_id: int) -> str:
        token = secrets.token_urlsafe(32)
        self._tokens[token] = {
            "user_id": user_id,
            "expires_at": datetime.now() + timedelta(hours=self.ttl_hours),
        }
        return token

    def validate_token(self, token: str) -> Optional[int]:
        data = self._tokens.get(token)
        if not data:
            return None
        if datetime.now() > data["expires_at"]:
            del self._tokens[token]
            return None
        return data["user_id"]

    def revoke_token(self, token: str):
        self._tokens.pop(token, None)


class AuthService:
    """Coordinates authentication flow."""

    def __init__(self, user_repo: UserRepository, user_cache: UserCache, token_mgr: TokenManager):
        self.user_repo = user_repo
        self.user_cache = user_cache
        self.token_mgr = token_mgr

    def authenticate(self, email: str, password: str) -> Optional[str]:
        user = self.user_repo.find_by_email(email)
        if not user or not user.is_active:
            return None
        # In real app, verify password against stored hash
        token = self.token_mgr.create_token(user.id)
        self.user_cache.set_user(user)
        return token

    def get_current_user(self, token: str) -> Optional[User]:
        user_id = self.token_mgr.validate_token(token)
        if user_id is None:
            return None
        user = self.user_cache.get_user(user_id)
        if user is None:
            user = self.user_repo.find_by_id(user_id)
            if user:
                self.user_cache.set_user(user)
        return user

    def logout(self, token: str):
        user_id = self.token_mgr.validate_token(token)
        if user_id:
            self.user_cache.invalidate(user_id)
        self.token_mgr.revoke_token(token)


def check_permission(user: User, resource_owner_id: int) -> bool:
    """Check if user can access a resource."""
    if user.is_admin():
        return True
    return user.id == resource_owner_id
