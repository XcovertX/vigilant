from grid import Grid, point_to_triangle, triangle_to_vertices
from math import isclose
import unittest

import unittest

class TestTriMapping(unittest.TestCase):

    def setUp(self):
        print("\n" + "=" * 60)
        print("Running TestTriMapping Suite")
        print("=" * 60)

    def test_rect_cells_and_roundtrip(self):
        print("\n[TEST] Rectangular Cells and Round-Trip Validation")
        cfg = Grid(rows=1, cols=2, w=150, h=100)
        cases = [
            ((10, 10), "A1"),
            ((140, 90), "A2"),
            ((160, 10), "A3"),
            ((290, 90), "A4"),
        ]
        for (x, y), expected in cases:
            result = point_to_triangle(cfg, x, y)
            status = "✅ PASS" if result == expected else "❌ FAIL"
            print(f"{status}: point_to_triangle({x:>5}, {y:>5}) → {result} (expected {expected})")
            self.assertEqual(result, expected)

        # Round-trip check
        print("\n[Round Trip] Verify triangle_to_vertices() + centroid → same designator")
        v = triangle_to_vertices(cfg, "A3")
        cx = sum(x for x, _ in v) / 3.0
        cy = sum(y for _, y in v) / 3.0
        result = point_to_triangle(cfg, cx, cy)
        print(f"Centroid ({cx:.1f}, {cy:.1f}) maps back to {result}")
        self.assertEqual(result, "A3")

    def test_on_diagonal_rule(self):
        print("\n[TEST] On-Diagonal Rule (TR→BL diagonal boundary)")
        cfg = Grid(rows=1, cols=1, w=100, h=100)
        x, y = 30, 70
        result = point_to_triangle(cfg, x, y)
        print(f"Diagonal point ({x},{y}) → {result} (expected A2)")
        self.assertEqual(result, "A2")  # by convention, assign to even/lower

    def test_out_of_bounds(self):
        print("\n[TEST] Out-of-Bounds Error Handling")
        cfg = Grid(rows=1, cols=1, w=100, h=100)

        print("Expecting exception for (-1, 0)")
        with self.assertRaises(Exception):
            point_to_triangle(cfg, -1, 0)
        print("✅ Exception caught as expected")

        print("Expecting exception for (1000, 1000)")
        with self.assertRaises(Exception):
            point_to_triangle(cfg, 1000, 1000)
        print("✅ Exception caught as expected")

def tri_area(verts):
    """Compute absolute area of triangle given vertices."""
    (x1, y1), (x2, y2), (x3, y3) = verts
    return abs(0.5 * (x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)))

def print_vertices_table(desig, verts):
    """Pretty-print triangle vertices."""
    print(f"\nVertices for {desig}")
    print("+---------+---------+")
    print("|    x    |    y    |")
    print("+---------+---------+")
    for x, y in verts:
        print(f"| {x:7.1f} | {y:7.1f} |")
    print("+---------+---------+")


class TestTriangleToVertices(unittest.TestCase):
    def setUp(self):
        print("\n" + "=" * 60)
        print("Running Triangle→Vertices and Round-Trip Tests")
        print("=" * 60)

    def test_vertices_odd_even_first_cell_square(self):
        print("\n[TEST] A1 (odd/upper) and A2 (even/lower) in 100x100 cell")
        cfg = Grid(rows=1, cols=1, w=100, h=100)

        v1 = triangle_to_vertices(cfg, "A1")
        print_vertices_table("A1", v1)
        self.assertEqual(v1, [(0, 0), (100, 0), (0, 100)])
        print(f"✅ A1 area = {tri_area(v1):.1f} (expected {cfg.w * cfg.h / 2:.1f})")
        self.assertTrue(isclose(tri_area(v1), cfg.w * cfg.h / 2.0))

        v2 = triangle_to_vertices(cfg, "A2")
        print_vertices_table("A2", v2)
        self.assertEqual(v2, [(100, 0), (0, 100), (100, 100)])
        print(f"✅ A2 area = {tri_area(v2):.1f} (expected {cfg.w * cfg.h / 2:.1f})")
        self.assertTrue(isclose(tri_area(v2), cfg.w * cfg.h / 2.0))

    def test_vertices_second_column_rect_cell(self):
        print("\n[TEST] B3 (odd) in row B, column 2, w≠h")
        cfg = Grid(rows=2, cols=2, w=150, h=100)
        v = triangle_to_vertices(cfg, "B3")
        print_vertices_table("B3", v)
        x0, y0 = 150, 100
        expected = [(x0, y0), (x0 + 150, y0), (x0, y0 + 100)]
        self.assertEqual(v, expected)
        print(f"✅ Area = {tri_area(v):.1f} (expected {cfg.w * cfg.h / 2:.1f})")

    def test_vertices_second_column_even_rect_cell(self):
        print("\n[TEST] A4 (even) in row A, column 2, w≠h")
        cfg = Grid(rows=2, cols=2, w=150, h=100)

if __name__ == "__main__":
    unittest.main(verbosity=2)
