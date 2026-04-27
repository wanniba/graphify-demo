# Graph Report - graphify-demo  (2026-04-27)

## Corpus Check
- 8 files · ~16,278 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 133 nodes · 421 edges · 7 communities detected
- Extraction: 34% EXTRACTED · 66% INFERRED · 0% AMBIGUOUS · INFERRED: 277 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `User` - 39 edges
2. `UserRepository` - 33 edges
3. `APIServer` - 32 edges
4. `AppConfig` - 29 edges
5. `Order` - 25 edges
6. `Product` - 24 edges
7. `UserCache` - 21 edges
8. `UserRole` - 21 edges
9. `REST API endpoints - the main entry point tying all modules together.` - 19 edges
10. `Main API server that wires all components together.` - 19 edges

## Surprising Connections (you probably didn't know these)
- `TokenManager` --uses--> `APIServer`  [INFERRED]
  app/auth.py → app/api.py
- `TokenManager` --uses--> `REST API endpoints - the main entry point tying all modules together.`  [INFERRED]
  app/auth.py → app/api.py
- `TokenManager` --uses--> `Main API server that wires all components together.`  [INFERRED]
  app/auth.py → app/api.py
- `AuthService` --uses--> `APIServer`  [INFERRED]
  app/auth.py → app/api.py
- `AuthService` --uses--> `REST API endpoints - the main entry point tying all modules together.`  [INFERRED]
  app/auth.py → app/api.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.16
Nodes (17): AuthService, check_permission(), hash(), PasswordHasher, Authentication and authorization module., Handles password hashing and verification., Manages authentication tokens., Coordinates authentication flow. (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (14): Main API server that wires all components together., DatabaseConnection, OrderRepository, ProductRepository, Database connection and query layer., Manages database connection pool., Establish connection pool., Data access for Product entities. (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (6): CacheClient, ProductCache, Redis caching layer for frequently accessed data., Caches product listings and individual products., AppConfig, Close all connections.

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (3): Notification, NotificationService, Orchestrates sending notifications across channels.

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (1): APIServer

### Community 5 - "Community 5"
Cohesion: 0.19
Nodes (7): REST API endpoints - the main entry point tying all modules together., Order, EmailSender, PushSender, Email and push notification service., Sends emails via SMTP., Sends push notifications via API.

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (6): DatabaseConfig, load_config(), NotificationConfig, Application configuration management., Load configuration from environment variables., RedisConfig

## Knowledge Gaps
- **6 isolated node(s):** `Data models for the application.`, `DatabaseConfig`, `RedisConfig`, `NotificationConfig`, `Application configuration management.` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 4`** (15 nodes): `APIServer`, `.get_product()`, `.get_user_orders()`, `.list_products()`, `.login()`, `.logout()`, `.authenticate()`, `.create_token()`, `.set()`, `.set_product()`, `.set_user()`, `.find_by_user()`, `.find_available()`, `.find_by_email()`, `.is_available()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `APIServer` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.187) - this node is a cross-community bridge._
- **Why does `User` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Why does `AppConfig` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `User` (e.g. with `PasswordHasher` and `TokenManager`) actually correct?**
  _`User` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `UserRepository` (e.g. with `PasswordHasher` and `TokenManager`) actually correct?**
  _`UserRepository` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `APIServer` (e.g. with `AuthService` and `CacheClient`) actually correct?**
  _`APIServer` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `AppConfig` (e.g. with `CacheClient` and `UserCache`) actually correct?**
  _`AppConfig` has 27 INFERRED edges - model-reasoned connections that need verification._