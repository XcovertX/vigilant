from pdb import main
import argparse

def main():
    print("AMRAS Triangle Mapper Console App")
    ap = argparse.ArgumentParser(description="AMRAS Triangle Mapper Console App")
    ap.add_argument('--rows', type=int, default=8, help='Number of grid rows (default: 8 for A..H)')
    ap.add_argument('--cols', type=int, default=8, help='Number of grid columns (default: 8 for 1..8)')
    args = ap.parse_args()
    print(f"Grid rows: {args.rows} (A..H)")
    print(f"Grid cols: {args.cols} (1..8)")

if __name__ == '__main__':
    main()