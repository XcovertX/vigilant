from dataclasses import dataclass

@dataclass
class Grid:
    rows: int
    cols: int
    w: float
    h: float

def print_grid(grid: Grid):
    for row in range(grid.rows):
        for col in range(grid.cols):
            print(f"({col * grid.w}, {row * grid.h})", end=" ")
        print()