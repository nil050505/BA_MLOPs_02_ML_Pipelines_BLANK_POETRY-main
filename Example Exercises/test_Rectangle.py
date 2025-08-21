from Rectangle import Rectangle
import unittest
class TestRectangleClass(unittest.TestCase):
    def setUp(self):
        # This rectangle will be created before each test method runs
        self.valid_rect = Rectangle(10, 5)

    def test_successful_initialization(self):
        # Test the setUp object
        self.assertEqual(self.valid_rect.width, 10)
        self.assertEqual(self.valid_rect.height, 5)

        # Test another valid one explicitly
        rect = Rectangle(1, 1)
        self.assertEqual(rect.width, 1)
        self.assertEqual(rect.height, 1)

    def test_value_error_on_non_positive_width(self):
        with self.assertRaisesRegex(ValueError, "Width and height must be positive."):
            Rectangle(0, 5)
        with self.assertRaisesRegex(ValueError, "Width and height must be positive."):
            Rectangle(-2, 5)

    def test_value_error_on_non_positive_height(self):
        with self.assertRaisesRegex(ValueError, "Width and height must be positive."):
            Rectangle(10, 0)
        with self.assertRaisesRegex(ValueError, "Width and height must be positive."):
            Rectangle(10, -5)

    def test_area_calculation(self):
        self.assertEqual(self.valid_rect.area(), 50) # 10 * 5

    def test_perimeter_calculation(self):
        self.assertEqual(self.valid_rect.perimeter(), 30) # 2 * (10 + 5)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)