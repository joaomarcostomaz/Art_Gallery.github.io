import unittest
import src.io_utils as io_utils
import src.triangulation as triangulation
import src.vertex_coloring as vertex_coloring

class TestPolygonFunctions(unittest.TestCase):

    def test_read_polygon_from_file(self):
        polygon = io_utils.read_polygon_from_file('test_polygon.csv')
        expected_polygon = [
            [0, 0], [1, 0], [1, 1], [0, 1]
        ]
        self.assertEqual(polygon, expected_polygon)

    def test_is_convex(self):
        self.assertTrue(triangulation.is_convex([0, 0], [1, 1], [2, 0]))
        self.assertFalse(triangulation.is_convex([0, 0], [1, -1], [2, 0]))

    def test_is_ear(self):
        polygon = [[0, 0], [1, 0], [1, 1], [0, 1]]
        self.assertTrue(triangulation.is_ear(polygon, 1))
        self.assertFalse(triangulation.is_ear(polygon, 0))

    def test_is_point_in_triangle(self):
        self.assertTrue(triangulation.is_point_in_triangle([0.5, 0.5], [0, 0], [1, 0], [0, 1]))
        self.assertFalse(triangulation.is_point_in_triangle([1.5, 1.5], [0, 0], [1, 0], [0, 1]))

    def test_ear_clipping_triangulation(self):
        polygon = [[0, 0], [1, 0], [1, 1], [0, 1]]
        expected_triangles = [[[0, 0], [1, 0], [0, 1]], [[1, 1], [0, 1], [1, 0]]]
        triangles = triangulation.ear_clipping_triangulation(polygon)
        self.assertEqual(triangles, expected_triangles)

    def test_color_vertices(self):
        triangles = [[[0, 0], [1, 0], [0, 1]], [[1, 1], [0, 1], [1, 0]]]
        coloring = vertex_coloring.color_vertices(triangles)
        expected_coloring = {(0, 0): 0, (1, 0): 1, (0, 1): 1, (1, 1): 0}
        self.assertEqual(coloring, expected_coloring)

    def test_find_minimum_cameras(self):
        coloring = {(0, 0): 0, (1, 0): 1, (0, 1): 1, (1, 1): 0}
        cameras = vertex_coloring.find_minimum_cameras(coloring)
        self.assertEqual(set(cameras), {(0, 0), (1, 1)})

if __name__ == '__main__':
    unittest.main()
