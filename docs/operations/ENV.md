# GEO Environment Variables

## Overview

This document describes all environment variables used by the GEO application. Variables are loaded from `backend/.env` file using Pydantic Settings.

---

## Quick Reference

```bash
# Minimum required for development
ANTHROPIC_API_KEY=sk-ant-xxx...

# Optional - sensible defaults provided
DATABASE_URL=sqlite+aiosqlite:///./geo.db
APP_ENV=development
DEBUG=true
```

---

## Variable Categories

### Application

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_NAME` | No | `GEO` | Application name |
| `APP_ENV` | No | `development` | Environment: development, staging, production |
| `DEBUG` | No | `true` | Enable debug mode and verbose logging |

### Server

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HOST` | No | `0.0.0.0` | Server bind host |
| `PORT` | No | `8000` | Server bind port |

### Database

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | No | `sqlite+aiosqlite:///./geo.db` | Database connection URL |
| `DB_POOL_SIZE` | No | `5` | Connection pool size |
| `DB_ECHO` | No | `false` | Log SQL queries (debug) |

**DATABASE_URL Formats**:

```bash
# SQLite (MVP default)
DATABASE_URL=sqlite+aiosqlite:///./geo.db

# PostgreSQL (production recommended)
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/geo
```

### Authentication

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | No | `change-this-...` | JWT signing key (min 32 chars) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | `7` | Refresh token lifetime |
| `ALGORITHM` | No | `HS256` | JWT algorithm |

> **Important**: Change `SECRET_KEY` in production!

### CORS

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CORS_ORIGINS` | No | `["http://localhost:3000", "http://localhost:5173"]` | Allowed origins |

### Claude API / Agent

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | **Yes** | - | Claude API key from Anthropic |
| `CLAUDE_MODEL` | No | `sonnet` | Model: sonnet, opus, haiku |
| `AGENT_WORKSPACE_DIR` | No | `/tmp/agent_workspaces` | Agent session workspace |
| `AGENT_MAX_TURNS` | No | `10` | Maximum conversation turns |
| `AGENT_TIMEOUT` | No | `300` | Request timeout (seconds) |

---

## Environment-Specific Values

### Development

```bash
# backend/.env
APP_ENV=development
DEBUG=true

# Database - SQLite for simplicity
DATABASE_URL=sqlite+aiosqlite:///./geo.db
DB_ECHO=false

# Security - OK to use defaults in dev
SECRET_KEY=dev-secret-key-not-for-production

# Claude API - Required
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Agent
AGENT_WORKSPACE_DIR=/tmp/agent_workspaces
```

### Staging

```bash
APP_ENV=staging
DEBUG=false

DATABASE_URL=postgresql+asyncpg://user:pass@staging-db:5432/geo
SECRET_KEY=<generated-staging-key>

ANTHROPIC_API_KEY=sk-ant-xxx
CORS_ORIGINS=["https://staging.geo-app.com"]
```

### Production

```bash
APP_ENV=production
DEBUG=false

DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/geo
SECRET_KEY=<generated-production-key>

ANTHROPIC_API_KEY=sk-ant-xxx
CORS_ORIGINS=["https://geo-app.com"]

# Tighter timeouts in production
AGENT_TIMEOUT=180
AGENT_MAX_TURNS=5
```

---

## Generating Secrets

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or using openssl
openssl rand -base64 32
```

---

## Getting API Keys

### Anthropic API Key

1. Sign up at https://console.anthropic.com/
2. Navigate to API Keys section
3. Create new API key
4. Copy key (starts with `sk-ant-`)

---

## Validation

The application validates environment variables on startup using Pydantic:

```python
from src.config.settings import settings

# Access settings
print(settings.app_env)
print(settings.database_url)
```

Invalid or missing required variables will cause startup failure:

```
pydantic_settings.SettingsError: 
  ANTHROPIC_API_KEY
    Field required [type=missing]
```

---

## Local Development

### Using .env file

```bash
# Copy example
cp backend/.env.example backend/.env

# Edit with your values
nano backend/.env
```

### Using shell export

```bash
# Export directly
export ANTHROPIC_API_KEY=sk-ant-xxx
export DEBUG=true

# Run application
make dev-backend
```

### Using direnv (recommended)

```bash
# Install direnv
brew install direnv  # macOS
sudo apt install direnv  # Ubuntu

# Create .envrc
echo "dotenv backend/.env" > .envrc

# Allow direnv
direnv allow
```

---

## Docker Environment

When using Docker Compose, pass environment variables:

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/geo
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
```

Or use env_file:

```yaml
services:
  backend:
    env_file:
      - backend/.env
```

---

## Security Best Practices

### Do

- Use strong, unique `SECRET_KEY` in production
- Store sensitive values in secrets manager
- Use environment-specific API keys
- Rotate secrets regularly

### Don't

- Commit `.env` files to git
- Use default `SECRET_KEY` in production
- Share API keys between environments
- Log sensitive values

---

## Adding New Variables

When adding a new environment variable:

1. Add to `backend/src/config/settings.py`:
   ```python
   class Settings(BaseSettings):
       new_variable: str = "default"
   ```

2. Add to this document with description

3. Add to `.env.example`:
   ```bash
   NEW_VARIABLE=example-value
   ```

4. Update deployment configurations

---

## Troubleshooting

### Variable not being read

```bash
# Check .env file exists
ls -la backend/.env

# Check file content
cat backend/.env

# Verify Python can read it
cd backend
python -c "from src.config.settings import settings; print(settings.app_env)"
```

### Database connection fails

```bash
# Verify DATABASE_URL format
echo $DATABASE_URL

# Test connection
cd backend
python -c "
from sqlalchemy import create_engine
engine = create_engine('$DATABASE_URL'.replace('+aiosqlite', ''))
with engine.connect() as conn:
    print('Connected!')
"
```

### API key not working

```bash
# Verify key is set
echo $ANTHROPIC_API_KEY

# Test API key
curl https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```
