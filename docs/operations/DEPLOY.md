# GEO Deployment Guide

## Deployment Overview

| Environment | Branch | Auto-Deploy | URL |
|-------------|--------|-------------|-----|
| Development | feature/* | No | localhost:8000 |
| Staging | develop | Yes (planned) | staging.geo-app.com |
| Production | main | Manual | geo-app.com |

---

## Quick Deploy

```bash
# Deploy to staging
make deploy-staging

# Deploy to production
make deploy-prod
```

---

## Deployment Methods

### Method 1: Docker Compose (Recommended for MVP)

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./data/geo.db
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

### Method 2: Manual Deploy

```bash
# 1. Build frontend
cd frontend && bun run build

# 2. Build backend image
cd backend && docker build -t geo-backend:latest .

# 3. Run migrations
docker run geo-backend:latest alembic upgrade head

# 4. Deploy backend
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="..." \
  -e ANTHROPIC_API_KEY="..." \
  geo-backend:latest

# 5. Serve frontend (nginx/CDN)
# Copy frontend/dist/* to web server
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing (`make test`)
- [ ] Code reviewed and approved
- [ ] Environment variables configured
- [ ] Database migrations tested
- [ ] API documentation updated
- [ ] CHANGELOG updated

### Post-Deployment

- [ ] Health check passing (`/health`)
- [ ] API docs accessible (`/api/docs`)
- [ ] Sample API calls working
- [ ] Monitoring alerts configured
- [ ] Team notified

---

## Environment Configuration

### Staging

```bash
# Set environment variables
export APP_ENV=staging
export DEBUG=false
export DATABASE_URL=postgresql+asyncpg://user:pass@staging-db:5432/geo
export SECRET_KEY=$(openssl rand -base64 32)
export ANTHROPIC_API_KEY=sk-ant-xxx
export CORS_ORIGINS='["https://staging.geo-app.com"]'
```

### Production

```bash
export APP_ENV=production
export DEBUG=false
export DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/geo
export SECRET_KEY=<from-secrets-manager>
export ANTHROPIC_API_KEY=<from-secrets-manager>
export CORS_ORIGINS='["https://geo-app.com"]'
```

---

## Database Migrations

### Before Deployment

```bash
# Generate migration (if needed)
cd backend
alembic revision --autogenerate -m "description"

# Test migration locally
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

### During Deployment

```bash
# Run migrations in production
docker run geo-backend:latest alembic upgrade head

# Or with docker-compose
docker-compose exec backend alembic upgrade head
```

### Rollback

```bash
# Rollback last migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade abc123
```

---

## Health Checks

### Endpoint

```bash
curl https://your-domain.com/health

# Expected response
{"status": "healthy"}
```

### Docker Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

---

## Monitoring

### Key Metrics to Watch

| Metric | Expected | Alert Threshold |
|--------|----------|-----------------|
| Response time (p95) | < 500ms | > 1000ms |
| Error rate | < 1% | > 5% |
| CPU usage | < 50% | > 80% |
| Memory usage | < 70% | > 90% |

### Logging

```bash
# View production logs
docker logs geo-backend -f

# Search for errors
docker logs geo-backend 2>&1 | grep -i error
```

---

## Rollback Procedures

### Application Rollback

```bash
# Tag current version before deploy
docker tag geo-backend:latest geo-backend:rollback

# If deploy fails, rollback
docker stop geo-backend
docker run -d --name geo-backend geo-backend:rollback
```

### Database Rollback

```bash
# Only if necessary and migration is reversible
docker-compose exec backend alembic downgrade -1

# WARNING: Some migrations are not reversible
```

---

## Chrome Extension Deployment

### Build for Production

```bash
cd extension
bun run build
```

### Submit to Chrome Web Store

1. Create ZIP of `extension/dist/`
2. Go to Chrome Web Store Developer Dashboard
3. Upload new version
4. Submit for review

### Local Distribution (Testing)

1. Share `extension/dist/` folder
2. Users load via `chrome://extensions/` → "Load unpacked"

---

## Security Considerations

### Secrets Management

- Never commit secrets to repository
- Use environment variables or secrets manager
- Rotate secrets regularly
- Use different secrets per environment

### Recommended Secrets Managers

| Platform | Service |
|----------|---------|
| AWS | Secrets Manager |
| GCP | Secret Manager |
| Azure | Key Vault |
| Generic | HashiCorp Vault |

### API Security

- Enable HTTPS only in production
- Configure proper CORS origins
- Implement rate limiting (planned)
- Add authentication (planned for v0.2)

---

## Scaling (Future)

### Horizontal Scaling

```yaml
# docker-compose with replicas
services:
  backend:
    deploy:
      replicas: 3
```

### Database Scaling

1. Migrate from SQLite to PostgreSQL
2. Add connection pooling (pgbouncer)
3. Consider read replicas for heavy read loads

### Caching Layer

1. Add Redis for caching
2. Cache frequently accessed data:
   - Visibility scores
   - Topic lists
   - Recommendation lists

---

## Troubleshooting Deployments

### Build Fails

```bash
# Check Docker build logs
docker-compose build --no-cache

# Verify Dockerfile syntax
docker build -t test ./backend
```

### Container Won't Start

```bash
# Check logs
docker logs geo-backend

# Common issues:
# - Missing environment variables
# - Port already in use
# - Database connection failed
```

### Health Check Fails

```bash
# Check inside container
docker exec -it geo-backend curl http://localhost:8000/health

# Check network
docker network ls
docker network inspect geo_default
```
