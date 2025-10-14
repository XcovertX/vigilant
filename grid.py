def print_grid(grid):
    for row in grid:
        print(" ".join(f"{cell:2}" for cell in row))