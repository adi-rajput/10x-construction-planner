# Coverage Planner – FastAPI, SQLite, HTML5 Canvas

This project implements a complete coverage-path planning system for rectangular walls with rectangular obstacles.  
The backend is built with FastAPI and stores computed trajectories in SQLite.  
The frontend uses HTML5 Canvas to visualize the wall, obstacles, and coverage path with playback animation.  
The project also includes request logging, performance timing, and API test cases.

---

## Overview

Coverage planning is typically used in robotics (e.g., painting drones, wall inspection robots, vacuum cleaners).  
The system takes user input:

- Wall dimensions (meters)  
- Rectangular obstacles (x, y, width, height)  
- Grid resolution  

It then converts the wall into a grid and computes a boustrophedon (zig-zag) sweep path that avoids obstacles.  
The path is stored in SQLite for visualization and retrieval.

The frontend allows:

- Displaying wall and obstacles  
- Drawing trajectory  
- Playback animation of the path  

---

## Features

### Backend
- FastAPI server with clean routing (modular structure)
- SQLite database using SQLAlchemy ORM
- CRUD operations for trajectory storage
- Automatic API documentation (Swagger UI)
- Request logging with timing
- CORS enabled for frontend communication

### Coverage Algorithm
- Grid-based boustrophedon sweep (zig-zag)
- Converts real-world dimensions to grid cells
- Removes obstacle cells
- Generates dense path points for coverage
- Supports adjustable resolution

### Frontend
- HTML5 Canvas 2D rendering
- Wall and obstacle visualization
- Trajectory line drawing
- Animated playback of path points
- Simple UI controls for create/load/play

### Testing
- API test suite using pytest + FastAPI TestClient
- Validates:
  - Trajectory creation
  - Listing
  - Fetching by ID
  - Deletion

---

## Project Structure

coverage_planner/
│── backend/
│ ├── init.py
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ ├── planner.py
│ ├── logger.py
│ └── routes/
│ └── trajectory.py
│
│── frontend/
│ ├── index.html
│ ├── script.js
│ └── styles.css
│
│── tests/
│ └── test_api.py
│
│── requirements.txt
│── .gitignore
│── README.md

yaml
Copy code

---

## Setup Instructions

### 1. Clone Repository
git clone https://github.com/your-username/coverage_planner.git
cd coverage_planner

shell
Copy code

### 2. Create Virtual Environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

shell
Copy code

### 3. Install Dependencies
pip install -r requirements.txt

shell
Copy code

### 4. Run Backend Server
uvicorn backend.main:app --reload

arduino
Copy code

Server runs at:
http://127.0.0.1:8000

yaml
Copy code

Swagger documentation:
http://127.0.0.1:8000/docs

shell
Copy code

### 5. Run Frontend

Inside the frontend folder:

cd frontend
python -m http.server 5500

r
Copy code

Open in browser:
http://127.0.0.1:5500

yaml
Copy code

---

## Coverage Planning Algorithm (Explanation)

1. The wall is divided into a grid based on the resolution (e.g., 0.1 m = 10 cm cells).  
2. Obstacle rectangles are mapped onto the grid and marked as blocked.  
3. The algorithm performs a boustrophedon sweep:
   - For even rows: left → right
   - For odd rows: right → left
4. Free cells generate center-points which form the coverage path.  
5. Consecutive duplicate points are removed to reduce noise.  
6. The final list of [x, y] coordinates is stored in the database.

---

## API Documentation

### POST /trajectory/create  
Creates a new trajectory by computing the coverage path.

Example body:
```json
{
  "name": "sample",
  "wall": { "width": 5, "height": 5 },
  "obstacles": [
    { "x": 1, "y": 1, "width": 0.25, "height": 0.25 }
  ],
  "resolution": 0.1
}
GET /trajectory/list
Returns stored trajectories.

GET /trajectory/{id}
Returns a specific trajectory including its path and metadata.

DELETE /trajectory/{id}
Deletes a trajectory.

Database Structure (SQLite)
Table: trajectories

Column	Type	Description
id	Integer PK	Auto-increment primary key
name	Text	User-provided name
path	JSON	List of [x, y] coordinates
meta	JSON	Wall + obstacle + resolution info
created_at	DateTime	Time of creation (indexed)

Index:

pgsql
Copy code
CREATE INDEX idx_created_at ON trajectories(created_at);
Logging and Performance
The backend logs:

Request method

Endpoint

HTTP status

Processing time in milliseconds

Trajectory creation duration

Logs are written using a rotating file handler to:

lua
Copy code
coverage_planner.log
Testing with Pytest
Run the tests:

css
Copy code
pytest -q
The tests validate:

Creating a trajectory

Retrieving it

Deleting it

Response correctness

Response time sanity

CORS Explanation
The frontend runs on:

cpp
Copy code
http://127.0.0.1:5500
The backend runs on:

cpp
Copy code
http://127.0.0.1:8000
Browsers block cross-origin requests unless explicitly allowed.
CORS middleware is added in main.py:

python
Copy code
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Troubleshooting
1. "ModuleNotFoundError: backend"
Ensure:

There is a folder named backend/ in the project root

It contains an __init__.py file

You are running uvicorn from the project root

2. CORS blocked
Ensure CORS middleware is added in main.py.

3. Fetch fails on frontend
Ensure backend is running on port 8000.

Future Enhancements
Multiple obstacles input from frontend

Obstacle editing and UI controls

Smoothing the trajectory

Variable resolution (higher resolution near obstacles)

Export trajectory as CSV/GeoJSON

Live robot simulation

Deployment on Render/Netlify

License
This project is provided for educational and experimental purposes.