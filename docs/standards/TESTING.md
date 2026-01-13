# GEO Testing Guide

## Testing Philosophy

1. **Test behavior, not implementation** - Focus on what the code does, not how
2. **Fast feedback** - Tests should run quickly for rapid iteration
3. **Reliable** - Tests should be deterministic and not flaky
4. **Maintainable** - Tests should be easy to understand and update

---

## Test Structure

### Directory Layout

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── unit/                 # Unit tests
│   │   ├── modules/
│   │   │   ├── tracking/
│   │   │   │   ├── test_service.py
│   │   │   │   ├── test_calculator.py
│   │   │   ├── analysis/
│   │   │   ├── citation/
│   │   │   └── optimization/
│   ├── integration/          # Integration tests
│   │   ├── test_tracking_api.py
│   │   ├── test_analysis_api.py
│   │   └── test_full_flow.py
│   └── e2e/                  # End-to-end tests
│       └── test_upload_flow.py
```

### Test Types

| Type | Scope | Speed | Dependencies |
|------|-------|-------|--------------|
| Unit | Single function/class | Fast | Mocked |
| Integration | Multiple modules | Medium | Database |
| E2E | Full flow | Slow | All services |

---

## Running Tests

### All Tests

```bash
make test
# or
cd backend && pytest tests/ -v
```

### Specific Test Types

```bash
# Unit tests only
make test-unit
# or
pytest tests/unit/ -v

# Integration tests only
make test-integration
# or
pytest tests/integration/ -v
```

### Single Test File

```bash
pytest tests/unit/modules/tracking/test_service.py -v
```

### Single Test Function

```bash
pytest tests/unit/modules/tracking/test_service.py::test_upload_conversations -v
```

### With Coverage

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Test Configuration

### conftest.py

```python
# backend/tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config.database import Base


@pytest.fixture
async def db_session():
    """Create test database session."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
def sample_conversation():
    """Sample conversation data for testing."""
    return {
        "id": "test-conv-1",
        "session_id": "test-session",
        "platform": "chatgpt",
        "messages": [
            {"role": "user", "content": "What is Salesforce?"},
            {"role": "assistant", "content": "Salesforce is a CRM platform..."}
        ],
        "captured_at": "2026-01-13T10:00:00Z"
    }
```

### pytest.ini

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
filterwarnings =
    ignore::DeprecationWarning
```

---

## Writing Tests

### Unit Test Example

```python
# tests/unit/modules/tracking/test_calculator.py
import pytest
from src.modules.tracking.calculator import visibility_calculator


class TestVisibilityCalculator:
    """Tests for visibility score calculation."""
    
    def test_calculate_score_with_mentions(self):
        """Score should increase with more mentions."""
        # Arrange
        mentions = [
            {"sentiment": 0.8, "position": 1, "mention_type": "direct"},
            {"sentiment": 0.6, "position": 2, "mention_type": "indirect"},
        ]
        
        # Act
        score = visibility_calculator.calculate_score(mentions)
        
        # Assert
        assert 0 <= score <= 100
        assert score > 0  # Has mentions, should have score
    
    def test_calculate_score_empty_mentions(self):
        """Score should be zero with no mentions."""
        score = visibility_calculator.calculate_score([])
        assert score == 0
    
    def test_direct_mentions_weight_higher(self):
        """Direct mentions should have higher weight than indirect."""
        direct = [{"sentiment": 0.5, "position": 1, "mention_type": "direct"}]
        indirect = [{"sentiment": 0.5, "position": 1, "mention_type": "indirect"}]
        
        direct_score = visibility_calculator.calculate_score(direct)
        indirect_score = visibility_calculator.calculate_score(indirect)
        
        assert direct_score > indirect_score
```

### Integration Test Example

```python
# tests/integration/test_tracking_api.py
import pytest
from httpx import AsyncClient
from src.main import app


@pytest.fixture
async def client():
    """Create test HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


class TestTrackingAPI:
    """Integration tests for tracking API."""
    
    @pytest.mark.asyncio
    async def test_upload_conversations(self, client, sample_conversation):
        """Test conversation upload endpoint."""
        response = await client.post(
            "/api/tracking/upload",
            json={"conversations": [sample_conversation]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["received"] == 1
        assert data["processed"] == 1
    
    @pytest.mark.asyncio
    async def test_get_visibility(self, client, db_session):
        """Test visibility query endpoint."""
        # Setup: Create brand and mentions
        # ...
        
        response = await client.get(
            "/api/tracking/visibility",
            params={"brand": "TestBrand"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "current_score" in data
        assert "trend" in data
```

### Async Test Example

```python
# tests/unit/modules/tracking/test_service.py
import pytest
from src.modules.tracking.service import tracking_service


class TestTrackingService:
    """Tests for tracking service."""
    
    @pytest.mark.asyncio
    async def test_register_brand(self, db_session):
        """Test brand registration."""
        brand = await tracking_service.register_brand(
            db_session,
            name="TestBrand",
            category="Technology"
        )
        
        assert brand.id is not None
        assert brand.name == "TestBrand"
        assert brand.category == "Technology"
    
    @pytest.mark.asyncio
    async def test_register_duplicate_brand_raises(self, db_session):
        """Duplicate brand should raise error."""
        await tracking_service.register_brand(db_session, name="TestBrand")
        
        with pytest.raises(Exception):  # Specify actual exception
            await tracking_service.register_brand(db_session, name="TestBrand")
```

---

## Test Naming Conventions

### Test Functions

```python
def test_[what]_[condition]_[expected]():
    """Description of what is being tested."""
    pass

# Examples
def test_calculate_score_with_no_mentions_returns_zero():
    pass

def test_upload_conversations_with_invalid_data_raises_validation_error():
    pass

def test_get_visibility_for_unknown_brand_returns_empty_response():
    pass
```

### Test Classes

```python
class TestClassName:
    """Tests for ClassName."""
    pass

# Examples
class TestVisibilityCalculator:
    """Tests for visibility score calculation."""
    pass

class TestTrackingService:
    """Tests for tracking service methods."""
    pass
```

---

## Test Structure (AAA Pattern)

```python
def test_something():
    # Arrange - Set up test data and conditions
    user = create_test_user()
    input_data = {"name": "test"}
    
    # Act - Execute the code being tested
    result = service.do_something(user, input_data)
    
    # Assert - Verify the results
    assert result.status == "success"
    assert result.data is not None
```

---

## Mocking

### Using pytest-mock

```python
def test_with_mock(mocker):
    """Test with mocked dependency."""
    # Mock external API call
    mock_api = mocker.patch(
        "src.modules.tracking.service.external_api.call"
    )
    mock_api.return_value = {"status": "ok"}
    
    # Test code that uses the API
    result = tracking_service.process_data()
    
    # Verify mock was called
    mock_api.assert_called_once()
```

### Mocking Database

```python
@pytest.fixture
async def mock_db_session(mocker):
    """Mock database session."""
    mock_session = mocker.AsyncMock()
    mock_session.execute.return_value.scalars.return_value.all.return_value = []
    return mock_session
```

---

## Coverage Requirements

### Minimum Coverage Targets

| Component | Target |
|-----------|--------|
| Overall | 70% |
| Services | 80% |
| API Routes | 70% |
| Utilities | 60% |

### Generating Coverage Report

```bash
# Terminal report
pytest tests/ --cov=src --cov-report=term-missing

# HTML report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

---

## Frontend Testing

### Type Checking

```bash
cd frontend
bun run typecheck
```

### Component Tests (Future)

```typescript
// Example with React Testing Library
import { render, screen } from '@testing-library/react';
import { ChatMessage } from './ChatMessage';

test('renders message content', () => {
  render(<ChatMessage role="assistant" content="Hello" />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt -r requirements-dev.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: backend/coverage.xml
```

---

## Best Practices

### Do

- Write tests before or alongside code (TDD/BDD)
- Use descriptive test names
- Keep tests independent (no shared state)
- Test edge cases and error conditions
- Use fixtures for common setup
- Mock external dependencies

### Don't

- Test implementation details
- Write tests that depend on other tests
- Ignore flaky tests (fix them)
- Skip tests without good reason
- Test framework code (FastAPI, SQLAlchemy)
