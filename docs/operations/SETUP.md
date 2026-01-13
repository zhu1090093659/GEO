# GEO Development Setup Guide

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| Python | 3.11+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| Bun | 1.0+ | https://bun.sh/ |
| Git | 2.x | https://git-scm.com/ |
| Make | Any | Pre-installed on macOS/Linux |

### Optional Software

| Software | Purpose | Installation |
|----------|---------|--------------|
| Docker | Containerization | https://docs.docker.com/get-docker/ |
| Chrome | Extension testing | https://www.google.com/chrome/ |
| VS Code | Recommended IDE | https://code.visualstudio.com/ |

---

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd GEO

# 2. Install all dependencies
make install

# 3. Set up environment
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# 4. Run database migrations
make db-migrate

# 5. Start development servers
make dev
```

After starting, access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

---

## Detailed Setup

### Step 1: Clone Repository

```bash
git clone <repo-url>
cd GEO
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env
```

Edit `backend/.env` with your settings (see [ENV.md](ENV.md) for details):

```bash
# Required
ANTHROPIC_API_KEY=your-api-key-here

# Optional - defaults work for development
DATABASE_URL=sqlite+aiosqlite:///./geo.db
APP_ENV=development
DEBUG=true
```

### Step 3: Database Setup

```bash
# From backend directory with venv activated
alembic upgrade head
```

This creates `geo.db` with all required tables.

### Step 4: Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies with Bun
bun install
```

### Step 5: Extension Setup (Optional)

```bash
# Navigate to extension
cd ../extension

# Install dependencies
bun install

# Build extension
bun run build
```

To load the extension in Chrome:
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `extension/dist/` directory

### Step 6: Start Development Servers

From project root:

```bash
# Start both frontend and backend
make dev

# Or start individually:
make dev-backend   # Backend only (port 8000)
make dev-frontend  # Frontend only (port 3000)
```

---

## IDE Setup

### VS Code

Recommended extensions:
- Python (Microsoft)
- Pylance
- Ruff
- TypeScript Vue Plugin (Volar)
- Tailwind CSS IntelliSense
- REST Client

Settings (`.vscode/settings.json`):

```json
{
    "python.defaultInterpreterPath": "./backend/.venv/bin/python",
    "python.analysis.typeCheckingMode": "basic",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": true
    },
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    }
}
```

### PyCharm / IntelliJ

1. Open project directory
2. Configure Python interpreter: `backend/.venv/bin/python`
3. Mark `backend/src/` as Sources Root
4. Mark `backend/tests/` as Test Sources Root

---

## Common Issues

### Issue: Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
PORT=8001 make dev-backend
```

### Issue: Python module not found

```bash
# Ensure virtual environment is activated
source backend/.venv/bin/activate

# Verify Python path
which python
# Should show: .../backend/.venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Database migration fails

```bash
# Check current migration status
cd backend
alembic current

# Reset database (CAUTION: deletes data)
rm geo.db
alembic upgrade head
```

### Issue: Extension not capturing data

1. Verify extension is loaded in Chrome
2. Check Chrome DevTools console for errors
3. Ensure you're on a supported AI platform (chat.openai.com or claude.ai)
4. Verify DOM selectors in `extension/src/config/selectors.ts`

### Issue: Claude API errors

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Check .env file
cat backend/.env | grep ANTHROPIC

# Test API key (requires anthropic package)
python -c "import anthropic; c = anthropic.Anthropic(); print('OK')"
```

---

## Verification

Run these commands to verify setup:

```bash
# Backend health check
curl http://localhost:8000/health

# Expected: {"status": "healthy"}

# Run linting
make lint

# Run tests
make test
```

---

## Makefile Commands Reference

### Setup

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies |
| `make install-backend` | Install backend only |
| `make install-frontend` | Install frontend only |
| `make setup` | Full setup (install + db) |

### Development

| Command | Description |
|---------|-------------|
| `make dev` | Start frontend and backend |
| `make dev-backend` | Start backend only (port 8000) |
| `make dev-frontend` | Start frontend only (port 3000) |

### Testing

| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make test-backend` | Run backend tests |
| `make test-frontend` | Run frontend type check |
| `make lint` | Run all linters |
| `make format` | Format all code |
| `make check` | Run lint + test |

### Database

| Command | Description |
|---------|-------------|
| `make db-migrate` | Run migrations |
| `make db-rollback` | Rollback last migration |
| `make db-reset` | Reset database |
| `make db-status` | Show migration status |

### Build

| Command | Description |
|---------|-------------|
| `make build` | Build for production |
| `make build-frontend` | Build frontend only |
| `make build-backend` | Build backend Docker image |

### Utilities

| Command | Description |
|---------|-------------|
| `make clean` | Clean build artifacts |
| `make status` | Show project status |
| `make logs` | Show backend logs |

---

## Project Structure

```
GEO/
├── backend/
│   ├── .venv/              # Python virtual environment
│   ├── src/                # Source code
│   │   ├── api/            # API router
│   │   ├── config/         # Settings
│   │   └── modules/        # Business modules
│   ├── alembic/            # Migrations
│   ├── tests/              # Tests
│   ├── requirements.txt    # Dependencies
│   └── geo.db              # SQLite database (created)
├── frontend/
│   ├── src/                # React source
│   ├── node_modules/       # Dependencies (created)
│   └── dist/               # Build output (created)
├── extension/
│   ├── src/                # Extension source
│   └── dist/               # Build output (created)
├── docs/                   # Documentation
└── Makefile               # Task automation
```

---

## Next Steps

After setup is complete:

1. Read [OVERVIEW.md](../architecture/OVERVIEW.md) for system architecture
2. Review [API_EXTERNAL.md](../interfaces/API_EXTERNAL.md) for API documentation
3. Check [STATUS.md](../../STATUS.md) for current development status
4. Run `make status` to see project progress
