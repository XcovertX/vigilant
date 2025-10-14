from pdb import main
import argparse

from grid import Grid, print_grid

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
            print("point to tringle")
        elif choice == '2':
            print("triangle to vertices")
        elif choice == '3':
            print("Bye!")
            break

if __name__ == '__main__':
    main()