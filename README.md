### Universal Garment Pattern Construction Backend

This repository contains a headless, API-first backend for a **rule-based garment pattern construction engine**.  
The goal is to generate deterministic, parametric 2D patterns from measurements and drafting-school configurations, and expose them via a stateless HTTP API.

### Tech stack

- **Language**: Python 3.11+
- **Engine**: pure Python package `engine/` (no web/DB dependencies)
- **Web framework**: FastAPI (`app/main.py`, `app/api/`)
- **Database**: PostgreSQL (SQLAlchemy async models in `app/db/`)
- **Async processing**: Celery workers (`worker/`) with Redis broker/result backend
- **Exports**: SVG via `svgwrite` (DXF/PDF can be added later)
- **Containerization**: Docker + `docker-compose.yml`

### Key modules

- `engine/interface.py` – stable engine API (`PatternRequest`, `PatternGeometry`, `generate_pattern`, `export_pattern`)
- `engine/measurements/` – measurement models, units, validation
- `engine/anthropometry/` – body and size profiles (gender-neutral)
- `engine/formulas/` – small, safe DSL and evaluator for drafting formulas
- `engine/rules/` – rule graph (DAG) and executor to build geometry
- `engine/transforms/` – style/ease/darts/grading (pipeline scaffolding)
- `engine/geometry/` – points, lines, arcs, splines, pattern pieces, validation
- `engine/export/` – SVG exporter and export models
- `app/db/` – async SQLAlchemy models and session factory
- `app/services/` – orchestration services (patterns, subscriptions)
- `app/api/v1.py` – versioned FastAPI endpoints (`/v1/...`)
- `worker/` – Celery app and task stubs for async pattern generation

### Running locally (via Docker Compose)

```bash
docker compose up --build
```

This starts:
- `api` on port `8000` (FastAPI, Uvicorn)
- `worker` (Celery)
- `db` (PostgreSQL)
- `redis`

Once running, you can check:

- Health: `GET http://localhost:8000/health`
- Readiness: `GET http://localhost:8000/ready`

### Development notes

- The **engine is framework-agnostic** and can be reused as a standalone library.
- Drafting logic is **data-driven**: drafting schools, blocks, rule graphs, transforms, and profiles live as JSONB configs in Postgres.
- Async pattern generation and exports are intended to run via Celery workers using Redis queues; the current tasks are minimal stubs to be extended with real config loading and persistence.

### Tests

Run tests with:

```bash
pytest
```

Initial tests cover basic engine behavior and determinism; more golden-master, fuzz, and integration tests can be added as the rule/config set grows.
