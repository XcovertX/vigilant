from pdb import main
import argparse

from grid import Grid, point_to_triangle, print_grid, triangle_to_vertices

def main():
    print("AMRAS Triangle Mapper Console App")
    
    ap = argparse.ArgumentParser(description="AMRAS Triangle Mapper Console App")
    ap.add_argument('--rows', type=int, default=8, help='Number of grid rows (default: 8 for A..H)')
    ap.add_argument('--cols', type=int, default=8, help='Number of grid columns (default: 8 for 1..8)')
    ap.add_argument('--w', type=float, default=50, help='Square width in pixels')
    ap.add_argument('--h', type=float, default=40, help='Square height in pixels')
    args = ap.parse_args()

    grid = Grid(rows=args.rows, cols=args.cols, w=args.w, h=args.h)
    print_grid(grid)

    while True:
        print("Choose an option:\n  1) Point -> Triangle\n  2) Triangle -> Vertices\n  3) Quit")
        choice = input("> ").strip()
        if choice == '1':
            try:
                raw = input("Enter x y: ").strip()
                x_str, y_str = raw.split()
                x, y = float(x_str), float(y_str)
                desig = point_to_triangle(grid, x, y)
                print(f"Triangle: {desig}\n")
            except Exception as e:
                print(f"Error: {e}\n")
        elif choice == '2':
            try:
                desig = input("Enter triangle designator (e.g., A1): ").strip()
                verts = triangle_to_vertices(grid, desig)
                print("Vertices (x,y):")
                for v in verts:
                    print(f"  {v}")
                print()
            except Exception as e:
                print(f"Error: {e}\n")
        elif choice == '3':
            print("Bye!")
            break

if __name__ == '__main__':
    main()