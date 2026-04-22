# graphify-demo

A small multi-module Python project for testing [graphify](https://github.com/safishamsi/graphify) knowledge graph generation.

## Structure

```
app/
  api.py          - REST API endpoints (FastAPI)
  auth.py         - Authentication & authorization
  models.py       - Data models (User, Order, Product)
  db.py           - Database connection & queries
  cache.py        - Redis caching layer
  notifications.py - Email & push notification service
  config.py       - Configuration management
```

## Architecture

```
API → Auth → DB
 ↓         ↗
Cache   Models
 ↓
Notifications → Config
```

## Usage

```bash
graphify update .
# generates graphify-out/graph.html, graph.json, GRAPH_REPORT.md
```
