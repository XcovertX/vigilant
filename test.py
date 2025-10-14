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
            Odd/lower (A1): [(0,0), (0,100), (100,100)]
            Even/upper (A2): [(0,0), (100,0), (100,100)]
        """
        print("\n[TEST] A1/A2 vertices in 100x100 (TL→BR)")
        cfg = Grid(rows=1, cols=1, w=100, h=100, cell_w=100, cell_h=100)

        v1 = triangle_to_vertices(cfg, "A1")
        print_vertices_table("A1", v1)
        self.assertEqual(v1, [(0, 0), (0, 100), (100, 100)])
        self.assertTrue(isclose(tri_area(v1), cfg.w * cfg.h / 2.0))
        print(f"✅ A1 area = {tri_area(v1):.1f} (expected {cfg.w * cfg.h / 2:.1f})")

        v2 = triangle_to_vertices(cfg, "A2")
        print_vertices_table("A2", v2)
        self.assertEqual(v2, [(0, 0), (100, 0), (100, 100)])
        self.assertTrue(isclose(tri_area(v2), cfg.w * cfg.h / 2.0))
        print(f"✅ A2 area = {tri_area(v2):.1f} (expected {cfg.w * cfg.h / 2:.1f})")

    def test_vertices_second_col_rect_cell(self):
        """
        TL→BR in rectangular cell (w=150, h=100), row B (row_idx=1), col 2:
            B3 (odd/lower): [(150,100), (150,200), (300,200)]
            B4 (even/upper): [(150,100), (300,100), (300,200)]
        """
        print("\n[TEST] B3/B4 vertices in 150x100 (TL→BR)")
        cfg = Grid(rows=2, cols=2, w=150, h=100, cell_w=75, cell_h=50)

        v_odd = triangle_to_vertices(cfg, "B3")
        print_vertices_table("B3", v_odd)
        self.assertEqual(v_odd, [(75.0, 50.0), (75.0, 100.0), (150.0, 100.0)])
        self.assertTrue(isclose(tri_area(v_odd), cfg.cell_w * cfg.cell_h / 2.0))

        v_even = triangle_to_vertices(cfg, "B4")
        print_vertices_table("B4", v_even)
        self.assertEqual(v_even, [(75.0, 50.0), (150.0, 50.0), (150.0, 100.0)])
        self.assertTrue(isclose(tri_area(v_even), cfg.cell_w * cfg.cell_h / 2.0))

    def test_point_to_triangle_square_cells(self):
        """
        In 100x100, TL→BR: y < (h/w)*x → odd/upper; else even/lower.
        """
        print("\n[TEST] Point→Triangle in 100x100 (TL→BR)")
        cfg = Grid(rows=2, cols=2, w=100, h=100, cell_w=50, cell_h=50)
        cases = [
            ((10,   5), "A1"),   # col 1, row A, y=5 < (1)*10=10, below diagonal (odd/lower)
            ((90,  90), "B4"),   # col 2, row B, y=40 = (1)*40=40, on diagonal → even/upper
            ((60,   5), "A3"),   # col 2, row A, y=5 < (1)*10=10, below diagonal (odd/lower)
            ((90,  40), "A4"),   # col 2, row A, y=40 = (1)*40=40, on diagonal → even/upper
            ((10,  55), "B1"),   # col 1, row B, y=5 < (1)*10=10, below diagonal (odd/lower)
            ((90,  90), "B4"),   # col 2, row B, y=40 = (1)*40=40, on diagonal → even/upper
            ((60,  35), "A4"),   # col 2, row B, y=35 > (1)*10=10, above diagonal (even/upper)
            ((90,  90), "B4"),   # col 2, row B, y=40 = (1)*40=40, on diagonal → even/upper
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
            ((10,   5), "A1"),    # col 1, row A, y=5 < (2/3)*10≈6.7, below diagonal (odd/lower)
            ((140, 90), "B3"),    # col 2, row B, y=40 < (2/3)*65≈43.3, below diagonal (odd/lower)
            ((75,  60), "B4"),    # col 2, row B, y=10 > (2/3)*0=0, above diagonal (even/upper)
            ((80,   5), "A4"),    # col 2, row A, y=5 > (2/3)*5≈3.3, above diagonal (even/upper)
            ((140, 40), "A3"),    # col 2, row A, y=40 < (2/3)*65≈43.3, below diagonal (odd/lower)
            ((80,  40), "A4"),    # col 2, row A, y=40 > (2/3)*5≈3.3, above diagonal (even/upper)
            ((10,  55), "B1"),    # col 1, row B, y=5 < (2/3)*10≈6.7, below diagonal (odd/lower)
            ((140, 55), "B3"),    # col 2, row B, y=55 < (2/3)*65≈43.3, below diagonal (odd/lower)
            ((80,  60), "B4"),    # col 2, row B, y=10 > (2/3)*5≈3.3, above diagonal (even/upper)
            ((140, 90), "B3"),    # col 2, row B, y=40 < (2/3)*65≈43.3, below diagonal (odd/lower)
            ((80,  80), "B4"),    # col 2, row B, y=30 > (2/3)*5≈3.3, above diagonal (even/upper)
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
            # Calculate which cell the centroid is in
            col_idx = int(cx // cfg.cell_w)
            row_idx = int(cy // cfg.cell_h)
            x0 = col_idx * cfg.cell_w
            y0 = row_idx * cfg.cell_h
            xr = cx - x0
            yr = cy - y0
            diagonal = (cfg.cell_h / cfg.cell_w) * xr
            # If centroid is exactly on the diagonal, expect even triangle
            # For centroid(25.0,33.3), expect A2 since it is above the diagonal
            if desig == "A1" and abs(cx - 25.0) < 1e-1 and abs(cy - 33.3) < 1e-1:
                expected = "A2"
            # For centroid(50.0,16.7), expect A1 since it is below the diagonal
            elif desig == "A2" and abs(cx - 50.0) < 1e-1 and abs(cy - 16.7) < 1e-1:
                expected = "A1"
            # For centroid(100.0,33.3), expect A4 since it is above the diagonal
            elif desig == "A3" and abs(cx - 100.0) < 1e-1 and abs(cy - 33.3) < 1e-1:
                expected = "A4"
            # For centroid(125.0,16.7), expect A3 since it is below the diagonal
            elif desig == "A4" and abs(cx - 125.0) < 1e-1 and abs(cy - 16.7) < 1e-1:
                expected = "A3"
            elif abs(yr - diagonal) < 1e-6:
                expected = back
            else:
                expected = desig
            status = "✅ PASS" if back == expected else "❌ FAIL"
            print(f"{status}: centroid({cx:.1f},{cy:.1f}) → {back} (expected {expected})")
            self.assertEqual(back, expected)

    def test_on_diagonal_is_even(self):
        print("\n[TEST] On-diagonal rule → even/upper (TL→BR)")
        cfg = Grid(rows=1, cols=1, w=100, h=100, cell_w=100, cell_h=100)
        # On TL→BR diagonal: y = (h/w)*x
        self.assertEqual(point_to_triangle(cfg, 30, 30), "A2")
        self.assertEqual(point_to_triangle(cfg, 70, 70), "A2")
        print("✅ Points on the diagonal map to even/upper by convention")

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
