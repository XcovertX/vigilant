from dataclasses import dataclass

@dataclass
class Grid:
    rows: int
    cols: int
    w: float
    h: float

def print_grid(grid: Grid):
    print(f"Grid rows: {grid.rows}")
    print(f"Grid cols: {grid.cols}")
    print(f"Square width: {grid.w} pixels")
    print(f"Square height: {grid.h} pixels")

def row_letter(row_index: int) -> str:
    """0 -> 'A', 1 -> 'B', ... Supports up to 26 rows."""
    if not (0 <= row_index < 26):
        raise ValueError("row_index out of range (0..25)")
    return chr(ord('A') + row_index)

def point_to_triangle(cfg: Grid, x: float, y: float) -> str:
    """Given pixel coordinates (x,y), return triangle designator like 'A1'."""
    if x < 0 or y < 0:
        raise ValueError("Coordinates must be non-negative and within the grid bounds.")
    col_idx = int(x // cfg.w)  # figures out which column
    row_idx = int(y // cfg.h)  # figures out which row
    if col_idx >= cfg.cols or row_idx >= cfg.rows:
        raise ValueError("Point is outside the grid.")
    x0 = col_idx * cfg.w       # left edge of the square
    y0 = row_idx * cfg.h       # top edge of the square
    xr = x - x0                # relative x
    yr = y - y0                # relative y
    # Top Left -> Bottom Right diagonal: y = (h/w) * x
    # If the point is ABOVE the TL->BR diagonal, it's the odd/upper triangle; else even/lower.
    above = yr < (cfg.h / cfg.w) * xr
    tri_num = (2 * (col_idx + 1) - 1) if above else (2 * (col_idx + 1))
    return f"{row_letter(row_idx)}{tri_num}"