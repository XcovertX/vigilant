# vigilant

## main.py
`main.py` is a console application for mapping points and triangles in a grid. It allows you to:
- Convert pixel coordinates (x, y) to a triangle designator (e.g., A1)
- Convert a triangle designator to its vertex coordinates

### Usage
Run the app with customizable grid parameters:

```sh
python main.py --rows 10 --cols 10 --w 100 --h 100
```

You will be prompted to choose:
- Point → Triangle: Enter x and y coordinates to get the triangle designator
- Triangle → Vertices: Enter a triangle designator (e.g., A1) to get its vertices

## test.py
`test.py` contains unit tests for the grid mapping logic using Python's `unittest` framework.

### Running Tests
To run all tests and see console output for each case:

```sh
python -m unittest test.py
```

The tests cover:
- Mapping points to triangle designators for rectangular and square grids
- Round-trip validation (triangle centroid maps back to the same designator)
- Edge cases (points on the diagonal, out-of-bounds coordinates)