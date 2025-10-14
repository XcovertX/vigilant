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