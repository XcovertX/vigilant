# Vigilant -- Triangle Mapping Tool

## Overview
This project implements a console-based geometry application that maps between pixel coordinates and triangle designators within a rectangular grid. Each grid cell is divided into two right triangles along a **top-left → bottom-right (TL→BR)** diagonal.

The tool supports two complementary operations:

1. **Point → Triangle**  
   Given pixel coordinates `(x, y)`, the program determines which labeled triangle (e.g., `A1`, `B3`) the point lies within.

2. **Triangle → Vertices**  
   Given a triangle designator (e.g., `A1`), the program returns the coordinates of its three vertices, which fully define that triangle’s shape and position.  
   > **Interpretation:** Requirement 2 is implemented as *triangle → vertex coordinates*, not a list of every pixel within the triangle. This ensures the geometry is defined deterministically and can be inverted (used by Requirement 1).

---

## Coordinate System
- The coordinate origin `(0,0)` is located at the **top-left** corner.  
- Rows increase **downward** (`A`, `B`, `C`, …).  
- Columns increase **to the right** (`1`, `2`, `3`, …).  
- Each square cell has width `w` and height `h`.  
- Each cell is split by a **top-left → bottom-right (TL→BR)** diagonal.

```
Top-Left (x0, y0)
+---------+
| \       |   ← Odd / Upper (A1, A3, A5, …)
|  \      |
|   \     |   Diagonal: y = (h/w) * x
|    \    |
|     \   |   Even / Lower (A2, A4, A6, …)
+---------+
```

---

## Deterministic Mapping Rule
To guarantee a unique mapping for every point:

> If a point lies exactly on the diagonal (`y == (h/w) * x`), it is assigned to the **even/lower** triangle.

This ensures:
- No overlap between triangles  
- No unmapped pixels  
- Deterministic, repeatable results  

---

## Directory Structure
```
.
├── main.py        # Console interface for point→triangle and triangle→vertices
├── grid.py        # Core geometry and mapping logic
├── test.py        # Unit test suite with detailed CLI output
└── README.md      # Project documentation
```

---

## main.py
`main.py` provides an interactive command-line interface.

### Example Usage
```bash
python main.py --rows 10 --cols 10 --w 100 --h 100
```

You will be prompted to choose an action:
1. **Point → Triangle** — enter pixel coordinates `x y` (e.g., `120 85`) to get the corresponding triangle designator (e.g., `A3`).  
2. **Triangle → Vertices** — enter a triangle designator (e.g., `A3`) to list its vertex coordinates.  
3. **Quit** — exit the program.

### Sample Output
```
Grid: rows=10 (A..J), cols=10, w=100, h=100

Choose an option:
  1) Point → Triangle
  2) Triangle → Vertices
  3) Quit

> 1
Enter x y: 25 40
Triangle: A1
```

---

## grid.py
Implements the mapping logic and data structures.

### Key Functions
| Function | Description |
|-----------|--------------|
| `point_to_triangle(cfg, x, y)` | Given pixel coordinates `(x, y)`, returns the corresponding triangle designator (e.g., `A3`). |
| `triangle_to_vertices(cfg, desig)` | Given a designator (e.g., `A3`), returns the three vertex coordinates defining that triangle. |
| `row_letter(row_index)` | Converts a numeric row index to its alphabetical label. |
| `square_col_from_tri(tri_num)` | Maps a triangle number (1–N) to its parent square column. |
| `is_odd_triangle(tri_num)` | Returns True if the triangle is odd/upper, else False for even/lower. |

### Geometry

### Triangle Vertex Conventions
- Odd (lower) triangle vertices:  
  `[(x0, y0), (x0, y0 + cell_h), (x0 + cell_w, y0 + cell_h)]`
- Even (upper) triangle vertices:  
  `[(x0, y0), (x0 + cell_w, y0), (x0 + cell_w, y0 + cell_h)]`
- Edge case: `y == (cell_h/cell_w)*x` → even/upper (ensures coverage continuity)

### Area Calculation
- Each triangle has area: `cell_w * cell_h / 2.0`

---

## test.py
`test.py` includes a comprehensive test suite built on Python’s `unittest` module.  

### Run Tests
```bash
python -m unittest test.py -v
```


### What the Tests Cover
- Triangle → Vertices correctness for both square and rectangular grids
- Point → Triangle mapping for multiple rows/columns
- On-diagonal edge case behavior (always even/upper)
- Round-trip validation: centroid of a triangle maps back to its own designator (or correct on-diagonal assignment)
- Area invariance: every triangle has an area of `cell_w * cell_h / 2.0`
- Out-of-bounds coordinate and invalid designator handling

---

## Example Test Output

```
[TEST] Point→Triangle in 100x100 (TL→BR)
✅ PASS: point_to_triangle(  10,   5) → A1 (expected A1)
✅ PASS: point_to_triangle(  90,  90) → B4 (expected B4)
✅ PASS: point_to_triangle(  60,   5) → A3 (expected A3)
✅ PASS: point_to_triangle(  90,  40) → A4 (expected A4)
✅ PASS: point_to_triangle(  10,  55) → B1 (expected B1)
✅ PASS: point_to_triangle(  90,  90) → B4 (expected B4)
✅ PASS: point_to_triangle(  60,  35) → A4 (expected A4)
✅ PASS: point_to_triangle(  90,  90) → B4 (expected B4)
✅ Points on the diagonal map to even/upper by convention
✅ Exceptions caught as expected
```

---

## Design Decisions
- **Top-left → bottom-right (TL→BR)** diagonal orientation matches the geometry shown in the provided PDF.  
- Deterministic **“on-diagonal → even/lower”** assignment ensures continuous coverage without overlap or ambiguity.  
- Logic generalizes to any rectangular grid (`w ≠ h`).  
- Code is modular and extendable for visualization or alternate diagonal orientations.

---

## Requirements
- Python **3.8+**
- No external dependencies (only uses `dataclasses` and `unittest`)
