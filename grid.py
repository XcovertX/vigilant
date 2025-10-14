from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Grid:
    rows: int
    cols: int
    w: float
    h: float
    cell_w: float
    cell_h: float

def print_grid(grid: Grid):
    print(f"Grid rows: {grid.rows}")
    print(f"Grid cols: {grid.cols}")
    print(f"Total width:  {grid.w} pixels")
    print(f"Total height: {grid.h} pixels")
    print(f"Cell width:   {grid.cell_w} pixels")
    print(f"Cell height:  {grid.cell_h} pixels")

def row_letter(row_index: int) -> str:
    """0 -> 'A', 1 -> 'B', ... Supports up to 26 rows."""
    if not (0 <= row_index < 26):
        raise ValueError("row_index out of range (0..25)")
    return chr(ord('A') + row_index)

def point_to_triangle(grid: Grid, x: float, y: float) -> str:
    """Given pixel coordinates (x,y), return triangle designator like 'A1'."""
    if x < 0 or y < 0:
        raise ValueError(f"Coordinates must be non-negative and within the grid bounds. {x}, {y} is invalid.")
    col_idx = int(x // grid.cell_w)  # figures out which column
    row_idx = int(y // grid.cell_h)  # figures out which row
    if col_idx >= grid.cols or row_idx >= grid.rows:
        raise ValueError(f"Point is outside the grid. {x}, {y} exceeds grid bounds. Grid: {grid}")
    x0 = col_idx * grid.cell_w       # left edge of the square
    y0 = row_idx * grid.cell_h       # top edge of the square 
    xr = x - x0                # relative x
    yr = y - y0                # relative y
    # Top Left -> Bottom Right diagonal in a cell: y = (h/w) * x
    # If the point is ABOVE the TL -> BR diagonal, it's the odd/upper triangle; else even/lower.
    above = yr < (grid.cell_h / grid.cell_w) * xr
    tri_num = (2 * (col_idx + 1) - 1) if above else (2 * (col_idx + 1))
    return f"{row_letter(row_idx)}{tri_num}"

def parse_designator(desig: str) -> Tuple[int, int]:
    """Parse a triangle designator like 'A1' into (row_index, triangle_number)."""
    if not desig or not desig[0].isalpha():
        raise ValueError("Invalid designator: must start with a letter")
    i = 0
    while i < len(desig) and desig[i].isalpha():
        i += 1
    row_str = desig[:i]
    num_str = desig[i:]
    if not num_str.isdigit():
        raise ValueError("Invalid designator: missing numeric part")
    row_idx = ord(row_str) - ord('A')
    tri_num = int(num_str)
    return row_idx, tri_num

def square_col_from_tri(tri_num: int) -> int:
    """Given a triangle number, return the 1-based square column it belongs to."""
    if tri_num < 1:
        raise ValueError("Triangle number must be >= 1")
    # two triangles per square column: odd/even
    return (tri_num + 1) // 2

def is_odd_triangle(tri_num: int) -> bool:
    """Return True if the triangle number is odd (upper triangle), else False (even, lower triangle)."""
    return (tri_num % 2) == 1

def square_top_left(grid: Grid, row_idx: int, square_col: int) -> Tuple[float, float]:
    """Return the (x0,y0) coordinates of the top-left corner of the given square cell."""
    if not (0 <= row_idx < grid.rows):
        raise ValueError("Row index out of bounds")
    if not (1 <= square_col <= grid.cols):
        raise ValueError("Square column out of bounds")
    x0 = (square_col - 1) * grid.cell_w
    y0 = row_idx * grid.cell_h
    return x0, y0

def triangle_to_vertices(grid: Grid, desig: str) -> List[Tuple[float, float]]:
    """Given a triangle designator like 'A1', return list of its vertices [(x1,y1), (x2,y2), (x3,y3)]."""
    row_idx, tri_num = parse_designator(desig)
    square_col = square_col_from_tri(tri_num)
    x0, y0 = square_top_left(grid, row_idx, square_col)

    # Odd = lower triangle (below TL->BR diagonal)
    if (tri_num % 2) == 1:
        return [(x0, y0), (x0, y0 + grid.cell_h), (x0 + grid.cell_w, y0 + grid.cell_h)]
    else:  # even/upper
        return [(x0, y0), (x0 + grid.cell_w, y0), (x0 + grid.cell_w, y0 + grid.cell_h)]

