from pdb import main
import argparse

def main():
    print("AMRAS Triangle Mapper Console App")
    ap = argparse.ArgumentParser(description="AMRAS Triangle Mapper Console App")
    ap.add_argument('--rows', type=int, default=8, help='Number of grid rows (default: 8 for A..H)')
    args = ap.parse_args()
    print(f"Grid rows: {args.rows} (A..)")
    
if __name__ == '__main__':
    main()