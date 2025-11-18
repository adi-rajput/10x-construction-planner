# backend/planner.py
from typing import List, Dict, Tuple
import math

def generate_coverage_path(wall: Dict, obstacles: List[Dict], resolution: float = 0.1) -> List[List[float]]:
    """
    wall: {"width":float,"height":float}
    obstacles: list of {"x","y","width","height"} bottom-left coords in meters
    resolution: grid cell size in meters (e.g., 0.1 = 10cm)
    Returns list of [x,y] points in meters (world coords)
    """

    w, h = wall["width"], wall["height"]
    cols = int(math.ceil(w / resolution))
    rows = int(math.ceil(h / resolution))

    # grid: False = free, True = blocked
    grid = [[False for _ in range(cols)] for __ in range(rows)]

    # helper: position of grid cell center at (r,c)
    def cell_center(r, c):
        x = (c + 0.5) * resolution
        y = (r + 0.5) * resolution
        return [round(x, 4), round(y, 4)]

    # mark obstacles
    for obs in obstacles:
        ox, oy, ow, oh = obs["x"], obs["y"], obs["width"], obs["height"]
        c0 = int(math.floor(ox / resolution))
        r0 = int(math.floor(oy / resolution))
        c1 = int(math.ceil((ox + ow) / resolution))
        r1 = int(math.ceil((oy + oh) / resolution))
        for r in range(r0, min(rows, r1)):
            for c in range(c0, min(cols, c1)):
                if 0 <= r < rows and 0 <= c < cols:
                    grid[r][c] = True

    # sweep rows bottom->top (r=0 bottom). Zig-zag left->right then right->left
    path = []
    for r in range(rows):
        cols_range = range(cols) if (r % 2 == 0) else range(cols - 1, -1, -1)
        row_points = []
        for c in cols_range:
            if not grid[r][c]:
                row_points.append(cell_center(r, c))
        # add row points in order, but only if contiguous in x direction
        if row_points:
            path.extend(row_points)

    # Optional: prune consecutive duplicates (if any)
    compact = []
    prev = None
    for p in path:
        if prev is None or p != prev:
            compact.append(p)
        prev = p
    return compact
