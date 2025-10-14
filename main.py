from pdb import main
import argparse

def main():
    print("AMRAS Triangle Mapper Console App")
    ap = argparse.ArgumentParser(description="AMRAS Triangle Mapper Console App")
    ap.add_argument('--rows', type=int, default=8, help='Number of grid rows (default: 8 for A..H)')
    ap.add_argument('--cols', type=int, default=8, help='Number of grid columns (default: 8 for 1..8)')
    ap.add_argument('--w', type=float, default=50, help='Square width in pixels')
    ap.add_argument('--h', type=float, default=40, help='Square height in pixels')
    args = ap.parse_args()
    print(f"Grid rows: {args.rows} (A..H)")
    print(f"Grid cols: {args.cols} (1..8)")
    print(f"Square width: {args.w} pixels")
    print(f"Square height: {args.h} pixels")

if __name__ == '__main__':
    main()