from grid import Grid, point_to_triangle, triangle_to_vertices
import unittest, math

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

if __name__ == "__main__":
    unittest.main(verbosity=2)
