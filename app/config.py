"""Application configuration management."""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    name: str = "graphify_demo"
    user: str = "admin"
    password: str = ""
    pool_size: int = 10


@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    ttl: int = 300


@dataclass
class NotificationConfig:
    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    from_email: str = "noreply@example.com"
    push_api_url: str = "https://push.example.com/api/v1"
    push_api_key: str = ""


@dataclass
class AppConfig:
    debug: bool = False
    secret_key: str = "change-me"
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    notification: NotificationConfig = field(default_factory=NotificationConfig)


def load_config() -> AppConfig:
    """Load configuration from environment variables."""
    config = AppConfig(
        debug=os.getenv("DEBUG", "false").lower() == "true",
        secret_key=os.getenv("SECRET_KEY", "change-me"),
    )
    config.database.host = os.getenv("DB_HOST", config.database.host)
    config.database.password = os.getenv("DB_PASSWORD", "")
    config.redis.host = os.getenv("REDIS_HOST", config.redis.host)
    config.notification.push_api_key = os.getenv("PUSH_API_KEY", "")
    return config
