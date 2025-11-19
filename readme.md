# Coverage Planner

> FastAPI • SQLite • HTML5 Canvas • Deployed on Netlify & Render

A coverage-path planning system for rectangular walls with obstacles. Computes boustrophedon sweep paths for robotics applications.

## Live Demo

- **Frontend:** [https://YOUR_NETLIFY_SITE.netlify.app](https://YOUR_NETLIFY_SITE.netlify.app)
- **API:** [https://YOUR_RENDER_BACKEND.onrender.com](https://YOUR_RENDER_BACKEND.onrender.com)
- **Docs:** [https://YOUR_RENDER_BACKEND.onrender.com/docs](https://YOUR_RENDER_BACKEND.onrender.com/docs)

---

## Features

- Grid-based boustrophedon sweep algorithm with obstacle avoidance
- RESTful API with FastAPI and SQLite storage
- Real-time Canvas visualization with playback animation
- Automatic Swagger documentation
- Full pytest test coverage

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/adi-rajput/10x-construction-planner.git
cd 10x-construction-planner
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run backend (Terminal 1)
uvicorn backend.main:app --reload
# → http://127.0.0.1:8000
# → http://127.0.0.1:8000/docs

# Run frontend (Terminal 2)
cd frontend
python -m http.server 5500
# → http://127.0.0.1:5500
```

---

## Project Structure

```
10x-construction-planner/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # SQLAlchemy config
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   ├── planner.py           # Coverage algorithm
│   ├── logger.py            # Logging setup
│   └── routes/
│       └── trajectory.py    # API routes
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── tests/
│   └── test_api.py
├── requirements.txt
└── Procfile
```

---

## API Reference

### Create Trajectory
```http
POST /trajectory/create

{
  "name": "sample",
  "wall": { "width": 5, "height": 5 },
  "obstacles": [
    { "x": 1, "y": 1, "width": 0.5, "height": 0.5 }
  ],
  "resolution": 0.1
}
```

### List All
```http
GET /trajectory/list
```

### Get by ID
```http
GET /trajectory/{id}
```

### Delete
```http
DELETE /trajectory/{id}
```

---

## Algorithm

1. Divide wall into grid cells (based on resolution)
2. Mark obstacle cells as blocked
3. Sweep pattern:
   - Even rows: left → right
   - Odd rows: right → left
4. Collect free cell centers as waypoints
5. Remove consecutive duplicates
6. Store as JSON in SQLite

---

## Database Schema

**Table: `trajectories`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key (auto-increment) |
| `name` | Text | Trajectory name |
| `path` | JSON | Array of [x, y] coordinates |
| `meta` | JSON | Wall dimensions, obstacles, resolution |
| `created_at` | DateTime | Timestamp (indexed) |

---

## Testing

```bash
pytest -q
```

Tests cover:
- Trajectory creation, listing, retrieval, deletion
- Response validation and timing

---

## Deployment

### Backend (Render)

**Procfile:**
```
web: uvicorn backend.main:app --host=0.0.0.0 --port=$PORT
```

**CORS in `backend/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://YOUR_NETLIFY_SITE.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend (Netlify)

**Publish directory:** `frontend/`

**Update `script.js`:**
```javascript
const API = "https://YOUR_RENDER_BACKEND.onrender.com/trajectory";
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: backend` | Run `uvicorn` from project root; ensure `backend/__init__.py` exists |
| CORS Error | Add Netlify domain to `allow_origins` in `main.py` |
| 404 Not Found | Check API URL includes `/trajectory` prefix |
| Frontend not updating | Hard refresh (Ctrl+Shift+R) or redeploy |

---
