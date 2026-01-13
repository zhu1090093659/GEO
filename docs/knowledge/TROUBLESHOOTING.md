# GEO Troubleshooting Guide

## Quick Diagnostics

### Health Check Commands

```bash
# Check backend health
curl http://localhost:8000/health

# Check API docs are accessible
curl http://localhost:8000/api/docs

# Check database connection
cd backend && python -c "
from src.config.database import get_db
import asyncio
async def check():
    async for db in get_db():
        print('Database OK')
        break
asyncio.run(check())
"

# Check environment
cd backend && python -c "from src.config.settings import settings; print(f'Env: {settings.app_env}')"
```

---

## Common Issues

### Development Environment

#### Issue: Backend fails to start

**Symptoms**:
```
ModuleNotFoundError: No module named 'src'
```

**Causes**:
1. Virtual environment not activated
2. PYTHONPATH not set
3. Dependencies not installed

**Solutions**:
```bash
# Activate virtual environment
cd backend
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Verify activation
which python  # Should show .venv path

# Reinstall dependencies
pip install -r requirements.txt

# Or use uvicorn with module path
cd backend && uvicorn src.main:app --reload
```

---

#### Issue: Database migration fails

**Symptoms**:
```
alembic.util.exc.CommandError: Target database is not up to date
sqlalchemy.exc.OperationalError: no such table
```

**Causes**:
1. Database out of sync with migrations
2. Corrupted migration history
3. Missing migration files

**Solutions**:
```bash
cd backend

# Check current migration status
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# If corrupted, reset database (WARNING: deletes all data)
rm geo.db
alembic upgrade head
```

---

#### Issue: Frontend cannot connect to backend

**Symptoms**:
```
Network Error
CORS error in browser console
```

**Causes**:
1. Backend not running
2. Wrong port configuration
3. CORS not configured

**Solutions**:
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/.env
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Restart backend after changing .env
make dev-backend
```

---

### Browser Extension

#### Issue: Extension not capturing conversations

**Symptoms**:
- Extension shows "No data captured"
- Upload API not being called
- Console shows selector errors

**Causes**:
1. AI platform updated DOM structure
2. Extension not loaded/enabled
3. Wrong platform detected

**Solutions**:

1. Check extension is loaded:
   - Open `chrome://extensions/`
   - Verify GEO extension is enabled
   - Click "Inspect" to view console

2. Check DOM selectors:
   ```typescript
   // extension/src/config/selectors.ts
   // Verify selectors match current AI platform structure
   
   export const CHATGPT_SELECTORS = {
       conversation: '[data-testid="conversation-turn"]',
       userMessage: '[data-message-author-role="user"]',
       assistantMessage: '[data-message-author-role="assistant"]',
   };
   ```

3. Update selectors if platform changed:
   - Open AI platform in Chrome
   - Right-click → Inspect Element
   - Find correct selectors for messages
   - Update `selectors.ts`

---

#### Issue: Extension upload fails

**Symptoms**:
```
Failed to upload conversations
Network error in extension popup
```

**Causes**:
1. Backend not running
2. API endpoint changed
3. Authentication issues (future)

**Solutions**:
```bash
# Verify backend is accessible from extension
curl -X POST http://localhost:8000/api/tracking/upload \
  -H "Content-Type: application/json" \
  -d '{"conversations": []}'

# Check extension API configuration
# extension/src/utils/api.ts
const API_BASE = 'http://localhost:8000/api';
```

---

### Claude API / Agent

#### Issue: Agent returns empty responses

**Symptoms**:
```
POST /chat/message returns nothing
SSE stream ends immediately
```

**Causes**:
1. `ANTHROPIC_API_KEY` not set or invalid
2. Claude Code CLI not installed
3. API rate limit exceeded

**Solutions**:
```bash
# Verify API key
echo $ANTHROPIC_API_KEY
# Should start with sk-ant-

# Test API key directly
curl https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"

# Verify Claude Code CLI is installed
claude --version

# If not installed
npm install -g @anthropic-ai/claude-code
```

---

#### Issue: Agent workspace permission denied

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
Failed to create workspace directory
```

**Causes**:
1. `AGENT_WORKSPACE_DIR` not writable
2. Directory doesn't exist
3. Docker volume permissions

**Solutions**:
```bash
# Check workspace directory
echo $AGENT_WORKSPACE_DIR
ls -la /tmp/agent_workspaces

# Create directory with permissions
mkdir -p /tmp/agent_workspaces
chmod 755 /tmp/agent_workspaces

# Or change workspace directory in .env
AGENT_WORKSPACE_DIR=/path/to/writable/directory
```

---

### API Issues

#### Issue: API returns 422 Validation Error

**Symptoms**:
```json
{
    "detail": [
        {
            "loc": ["body", "field_name"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

**Causes**:
1. Missing required fields
2. Wrong data types
3. Invalid enum values

**Solutions**:
- Check API documentation at `/api/docs`
- Verify request body matches schema
- Check Pydantic schema in `modules/*/schemas.py`

---

#### Issue: API returns 500 Internal Server Error

**Symptoms**:
```
500 Internal Server Error
Generic error message
```

**Diagnosis**:
```bash
# Enable debug mode
DEBUG=true make dev-backend

# Check logs
tail -f backend/logs/app.log

# Or check console output
# Backend logs show full stack trace in debug mode
```

**Common Causes**:

| Cause | Check | Fix |
|-------|-------|-----|
| Database down | `make db-status` | Restart database |
| Missing table | `alembic current` | Run migrations |
| Invalid query | Check logs | Fix service code |
| External API fail | Check Claude API | Verify API key |

---

### Performance Issues

#### Issue: Slow API responses

**Symptoms**:
- Requests taking > 1 second
- Timeouts occurring
- Database queries slow

**Diagnosis**:
```bash
# Enable SQL logging
DB_ECHO=true make dev-backend

# Check for N+1 queries in output
```

**Common Causes**:

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| N+1 queries | Check SQL log | Add eager loading |
| Missing index | EXPLAIN query | Add database index |
| Large response | Check payload size | Add pagination |
| Full table scan | Check query plan | Optimize query |

**Solutions**:
```python
# Add eager loading
from sqlalchemy.orm import selectinload

query = select(Brand).options(
    selectinload(Brand.mentions)
)

# Add index to model
class BrandMention(Base):
    __table_args__ = (
        Index('idx_brand_mentions_brand_id', 'brand_id'),
    )
```

---

#### Issue: High memory usage

**Symptoms**:
- Memory grows over time
- OOM errors
- Slow garbage collection

**Solutions**:
```bash
# Monitor memory
docker stats  # If using Docker
ps aux | grep python  # Check process memory

# Profile memory
pip install memory-profiler
python -m memory_profiler src/main.py
```

---

## GEO-Specific Issues

### Issue: Brand not detected in responses

**Symptoms**:
- Brand exists in database
- AI mentions brand in response
- No brand_mention record created

**Causes**:
1. Brand name case mismatch
2. Missing aliases
3. Detection algorithm issue

**Solutions**:
```bash
# Check brand registration
curl "http://localhost:8000/api/tracking/brands"

# Add aliases for brand
curl -X POST http://localhost:8000/api/tracking/brands \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Salesforce",
    "aliases": ["SFDC", "salesforce.com", "Salesforce CRM"]
  }'
```

---

### Issue: Visibility score not updating

**Symptoms**:
- New mentions added
- Score remains the same
- Trend data outdated

**Causes**:
1. Score calculation not triggered
2. Date filter issues
3. Cache (if implemented)

**Solutions**:
```bash
# Manually trigger score calculation
curl -X POST "http://localhost:8000/api/tracking/calculate-scores"

# Check with specific date
curl -X POST "http://localhost:8000/api/tracking/calculate-scores?date=2026-01-13"

# Verify scores updated
curl "http://localhost:8000/api/tracking/visibility?brand=YourBrand"
```

---

### Issue: llms.txt generation fails

**Symptoms**:
- POST /optimization/llms-txt returns error
- Empty content generated
- Invalid format

**Causes**:
1. Invalid URL provided
2. Missing required fields
3. Template error

**Solutions**:
```bash
# Verify request format
curl -X POST http://localhost:8000/api/optimization/llms-txt \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "site_name": "Example Site",
    "description": "A test site"
  }'
```

---

## Error Code Reference

| Error Code | Meaning | Common Fix |
|------------|---------|------------|
| 400 | Bad Request | Check request format |
| 404 | Not Found | Verify resource exists |
| 409 | Conflict | Resource already exists |
| 422 | Validation Error | Check required fields |
| 500 | Server Error | Check logs for details |

---

## Log Analysis

### Log Locations

| Environment | Location |
|-------------|----------|
| Development | Console output |
| Docker | `docker logs geo-backend` |
| Production | Configured log aggregation |

### Common Log Patterns

```bash
# Find errors
grep -i "error\|exception" logs/app.log

# Find slow queries (if DB_ECHO=true)
grep "SELECT\|INSERT\|UPDATE" logs/app.log | head -20

# Find specific request
grep "request_id=abc123" logs/app.log
```

---

## Getting Help

### Information to Gather

Before asking for help, collect:

1. **Error message** (full stack trace)
2. **Steps to reproduce**
3. **Environment** (local/staging/prod)
4. **Recent changes** (`git log --oneline -5`)
5. **Relevant logs**
6. **Request/response data** (if API issue)

### Escalation Path

1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Ask in team channel with collected info
4. Create detailed issue if new problem

---

## Adding New Entries

When you solve a new issue:

1. Document the symptoms
2. Document the diagnosis steps
3. Document the solution
4. Add to this guide
5. Consider if it indicates a systemic issue to fix
