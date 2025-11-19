# Coverage Planner – FastAPI, SQLite, HTML5 Canvas

A coverage-path planning system for rectangular walls with rectangular obstacles. Built with FastAPI backend, SQLite storage, and HTML5 Canvas frontend.

## Overview

Coverage planning is commonly used in robotics (painting drones, wall inspection robots, vacuum cleaners). This system takes user input for wall dimensions, obstacles, and grid resolution, then computes a boustrophedon (zig-zag) sweep path that avoids obstacles.

**Inputs:**
- Wall dimensions (meters)
- Rectangular obstacles (x, y, width, height)
- Grid resolution

**Outputs:**
- Coverage path stored in SQLite
- Visual representation on canvas
- Animated playback

## Features

**Backend:**
- FastAPI server with modular routing
- SQLite database using SQLAlchemy ORM
- CRUD operations for trajectory storage
- Swagger UI documentation at `/docs`
- Request logging with performance timing
- CORS enabled

**Coverage Algorithm:**
- Grid-based boustrophedon sweep
- Converts dimensions to grid cells
- Removes obstacle cells
- Generates waypoints for coverage
- Adjustable resolution

**Frontend:**
- HTML5 Canvas rendering
- Wall and obstacle visualization
- Trajectory line drawing
- Animated playback controls
- Simple UI for create/load/play operations

**Testing:**
- pytest test suite with FastAPI TestClient
- Tests for trajectory creation, listing, fetching, and deletion

## Project Structure

```
coverage_planner/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── planner.py
│   ├── logger.py
│   └── routes/
│       └── trajectory.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── tests/
│   └── test_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/coverage_planner.git
cd coverage_planner
```

### 2. Create Virtual Environment
**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Backend
```bash
uvicorn backend.main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

API docs at: `http://127.0.0.1:8000/docs`

### 5. Run Frontend
```bash
cd frontend
python -m http.server 5500
```

Open browser at: `http://127.0.0.1:5500`

## Algorithm

The coverage planning works as follows:

1. Wall is divided into a grid based on resolution (e.g., 0.1m = 10cm cells)
2. Obstacle rectangles are mapped to grid cells and marked as blocked
3. Boustrophedon sweep is performed:
   - Even rows: left to right
   - Odd rows: right to left
4. Free cells generate center points forming the coverage path
5. Consecutive duplicate points are removed
6. Final coordinates stored as JSON in database

## API Endpoints

### POST /trajectory/create
Creates a new trajectory.

**Request body:**
```json
{
  "name": "sample",
  "wall": { "width": 5, "height": 5 },
  "obstacles": [
    { "x": 1, "y": 1, "width": 0.25, "height": 0.25 }
  ],
  "resolution": 0.1
}
```

### GET /trajectory/list
Returns all stored trajectories.

### GET /trajectory/{id}
Returns specific trajectory with path data and metadata.

### DELETE /trajectory/{id}
Deletes a trajectory.

## Database Schema

**Table: trajectories**

| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Auto-increment primary key |
| name | Text | User-provided name |
| path | JSON | List of [x, y] coordinates |
| meta | JSON | Wall, obstacles, and resolution |
| created_at | DateTime | Timestamp (indexed) |

**Index:**
```sql
CREATE INDEX idx_created_at ON trajectories(created_at);
```

## Logging

The backend logs:
- Request method and endpoint
- HTTP status code
- Processing time (milliseconds)
- Trajectory computation duration

Logs written to: `coverage_planner.log` (rotating file handler)

## Testing

Run tests:
```bash
pytest -q
```

Tests validate:
- Trajectory creation
- Retrieval by ID
- Listing all trajectories
- Deletion
- Response correctness and timing

## CORS Configuration

Frontend runs on `http://127.0.0.1:5500`

Backend runs on `http://127.0.0.1:8000`

CORS middleware in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting

**"ModuleNotFoundError: backend"**
- Verify `backend/` folder exists in project root
- Ensure `__init__.py` exists in `backend/`
- Run `uvicorn` from project root

**CORS blocked**
- Check CORS middleware is added in `main.py`

**Frontend fetch fails**
- Verify backend is running on port 8000

## Future Enhancements

- Multiple obstacle input from frontend
- Obstacle editing UI
- Path smoothing algorithms
- Variable resolution (higher near obstacles)
- Export to CSV/GeoJSON
- Live robot simulation
- Cloud deployment (Render/Netlify)

## License

Educational and experimental use.