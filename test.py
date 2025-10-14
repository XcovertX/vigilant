import unittest
from math import isclose
from grid import Grid, triangle_to_vertices, point_to_triangle

def tri_area(verts):
    """Absolute area of triangle given vertices."""
    (x1, y1), (x2, y2), (x3, y3) = verts
    return abs(0.5 * (x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)))

def print_vertices_table(desig, verts):
    """Pretty-print triangle vertices for CLI readability."""
    print(f"\nVertices for {desig}")
    print("+---------+---------+")
    print("|    x    |    y    |")
    print("+---------+---------+")
    for x, y in verts:
        print(f"| {x:7.1f} | {y:7.1f} |")
    print("+---------+---------+")


class TestTLBRMapping(unittest.TestCase):

    def setUp(self):
        print("\n" + "=" * 64)
        print("Running TL→BR Triangle Mapping Tests")
        print("=" * 64)

    def test_vertices_first_cell_square(self):
        """
        TL→BR diagonal in a 100x100 cell:
          Odd/upper (A1): [(0,0), (100,0), (100,100)]
          Even/lower (A2): [(0,0), (0,100), (100,100)]
        """
        print("\n[TEST] A1/A2 vertices in 100x100 (TL→BR)")
        cfg = Grid(rows=1, cols=1, w=100, h=100, cell_w=100, cell_h=100)

        v1 = triangle_to_vertices(cfg, "A1")
        print_vertices_table("A1", v1)
        self.assertEqual(v1, [(0, 0), (100, 0), (100, 100)])
        self.assertTrue(isclose(tri_area(v1), cfg.w * cfg.h / 2.0))
        print(f"✅ A1 area = {tri_area(v1):.1f} (expected {cfg.w * cfg.h / 2:.1f})")

        v2 = triangle_to_vertices(cfg, "A2")
        print_vertices_table("A2", v2)
        self.assertEqual(v2, [(0, 0), (0, 100), (100, 100)])
        self.assertTrue(isclose(tri_area(v2), cfg.w * cfg.h / 2.0))
        print(f"✅ A2 area = {tri_area(v2):.1f} (expected {cfg.w * cfg.h / 2:.1f})")

    def test_vertices_second_col_rect_cell(self):
        """
        TL→BR in rectangular cell (w=150, h=100), row B (row_idx=1), col 2:
          B3 (odd/upper): [(150,100), (300,100), (300,200)]
          B4 (even/lower): [(150,100), (150,200), (300,200)]
        """
        print("\n[TEST] B3/B4 vertices in 150x100 (TL→BR)")
        cfg = Grid(rows=2, cols=2, w=150, h=100, cell_w=75, cell_h=50)

        v_odd = triangle_to_vertices(cfg, "B3")
        print_vertices_table("B3", v_odd)
        self.assertEqual(v_odd, [(150, 100), (300, 100), (300, 200)])
        self.assertTrue(isclose(tri_area(v_odd), cfg.w * cfg.h / 2.0))

        v_even = triangle_to_vertices(cfg, "B4")
        print_vertices_table("B4", v_even)
        self.assertEqual(v_even, [(150, 100), (150, 200), (300, 200)])
        self.assertTrue(isclose(tri_area(v_even), cfg.w * cfg.h / 2.0))

    def test_point_to_triangle_square_cells(self):
        """
        In 100x100, TL→BR: y < (h/w)*x → odd/upper; else even/lower.
        """
        print("\n[TEST] Point→Triangle in 100x100 (TL→BR)")
        cfg = Grid(rows=2, cols=2, w=100, h=100, cell_w=50, cell_h=50)
        cases = [
            ((10,   5), "A1"),   # col 1, row A, y=5 < (1)*10=10, above diagonal (odd)
            ((90,  90), "A2"),   # col 1, row A, y=90 = (1)*90=90, on diagonal → even/lower
            ((110,   5), "A3"),  # col 2, row A, y=5 < (1)*10=10, above diagonal (odd)
            ((190,  90), "A4"),  # col 2, row A, y=90 = (1)*90=90, on diagonal → even/lower
            ((10,  110), "B2"),  # col 1, row B, y=10 < (1)*10=10, above diagonal (odd)
            ((90,  190), "B2"),  # col 1, row B, y=90 = (1)*90=90, on diagonal → even/lower
            ((110, 105), "B3"),  # col 2, row B, y=5 < (1)*10=10, above diagonal (odd)
            ((190, 190), "B4"),  # col 2, row B, y=90 = (1)*90=90, on diagonal → even/lower
        ]
        for (x, y), expected in cases:
            got = point_to_triangle(cfg, x, y)
            status = "✅ PASS" if got == expected else "❌ FAIL"
            print(f"{status}: point_to_triangle({x:>4},{y:>4}) → {got} (expected {expected})")
            self.assertEqual(got, expected)

    def test_point_to_triangle_rect_cells(self):
        """
        In 150x100, TL→BR: slope = h/w = 2/3.
        """
        print("\n[TEST] Point→Triangle in 150x100 (TL→BR)")
        cfg = Grid(rows=2, cols=2, w=150, h=100, cell_w=75, cell_h=50)
        cases = [
            ((10,   5), "A1"),   # col 1, row A, y=5 < (2/3)*10≈6.7, above diagonal (odd)
            ((140, 90), "A1"),   # col 1, row A, y=90 < (2/3)*140≈93.3, above diagonal (odd)
            ((75,  60), "A2"),   # col 1, row A, y=60 > (2/3)*75=50, below diagonal (even)
            ((160,  5), "A3"),   # col 2, row A, y=5 < (2/3)*10≈6.7, above diagonal (odd)
            ((290, 90), "A3"),   # col 2, row A, y=90 < (2/3)*140≈93.3, above diagonal (odd)
            ((200, 90), "A4"),   # col 2, row A, y=90 > (2/3)*50≈33.3, below diagonal (even)
            ((160, 80), "A4"),   # col 2, row A, y=80 > (2/3)*10≈6.7, below diagonal (even)
            ((10, 110), "B2"),   # col 1, row B, y=10 > (2/3)*10≈6.7, below diagonal (even)
            ((140,190), "B1"),   # col 1, row B, y=90 < (2/3)*140≈93.3, above diagonal (odd)
            ((160,110), "B4"),   # col 2, row B, y=10 > (2/3)*10≈6.7, below diagonal (even)
            ((290,190), "B3"),   # col 2, row B, y=90 < (2/3)*140≈93.3, above diagonal (odd)
            ((200,180), "B4"),   # col 2, row B, y=80 > (2/3)*50≈33.3, below diagonal (even)
        ]
        for (x, y), expected in cases:
            got = point_to_triangle(cfg, x, y)
            status = "✅ PASS" if got == expected else "❌ FAIL"
            print(f"{status}: point_to_triangle({x:>4},{y:>4}) → {got} (expected {expected})")
            self.assertEqual(got, expected)

    def test_roundtrip_centroid_maps_back(self):
        print("\n[TEST] Centroid round-trip (TL→BR)")
        cfg = Grid(rows=1, cols=2, w=150, h=100, cell_w=75, cell_h=50)
        for desig in ("A1", "A2", "A3", "A4"):
            verts = triangle_to_vertices(cfg, desig)
            cx = sum(x for x, _ in verts) / 3.0
            cy = sum(y for _, y in verts) / 3.0
            back = point_to_triangle(cfg, cx, cy)
            status = "✅ PASS" if back == desig else "❌ FAIL"
            print(f"{status}: centroid({cx:.1f},{cy:.1f}) → {back} (expected {desig})")
            self.assertEqual(back, desig)

    def test_on_diagonal_is_even(self):
        print("\n[TEST] On-diagonal rule → even/lower (TL→BR)")
        cfg = Grid(rows=1, cols=1, w=100, h=100, cell_w=100, cell_h=100)
        # On TL→BR diagonal: y = (h/w)*x
        self.assertEqual(point_to_triangle(cfg, 30, 30), "A2")
        self.assertEqual(point_to_triangle(cfg, 70, 70), "A2")
        print("✅ Points on the diagonal map to even/lower by convention")

    def test_out_of_bounds(self):
        print("\n[TEST] Out-of-bounds handling")
        cfg = Grid(rows=1, cols=1, w=100, h=100, cell_w=100, cell_h=100)
        with self.assertRaises(Exception):
            _ = point_to_triangle(cfg, -1, 0)
        with self.assertRaises(Exception):
            _ = point_to_triangle(cfg, 1000, 1000)
        print("✅ Exceptions caught as expected")

if __name__ == "__main__":
    unittest.main(verbosity=2)
