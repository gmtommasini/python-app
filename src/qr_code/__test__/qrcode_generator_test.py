import unittest
from .. import qrcode_generator

import io
from PIL import Image
import qrcode

class create_qr(unittest.TestCase):
    def test_qr_base64(self):
        expected = 'iVBORw0KGgoAAAANSUhEUgAAAOYAAADmAQAAAADpEcQWAAABNElEQVR4nO2YQW7DIBBF35RIWZIb9Cjkar2ZfZTeAC8jYf0uDIlwkyibCKryFxHOW/hrNMD3mHis9eMJhP9G0XRbeUmTT+UPn/r03JB6SVICWI0QQZKkqWPPzehqZieA5Zh35GxmrV31TUO8Vq0jV33S+TM9oe9771+hB8AJWCF8H8tKbV31Set7MDHuwceyka9epluqKg9OhOhKyBp9tZOm7bxyIkTYVviEpFGrWlLMP+QyaWuu0Ve/JEll5+GUj3qfIIy+2knStt8gqDq5Rl/tpZuufVVKN2pVazdnIEiSotM42+/Qas6gidXAX8zOHXtuRus5w3KA2Q7o69Sx5+bUX4z5BHbegkMfrrqhXDM6ZSOWaDruwTvUKWfR5agcrWJ7V/3R6h4kB9LxjXNXY87wOv0BHOfQCtcfb3sAAAAASUVORK5CYII='
        result = qrcode_generator.create_qrcode("abc", base64encode=True, box_size=10, border=1)
        print("Result: ", result)
        self.assertEqual(result, expected)

    def test_qr_img_buffer(self):
        data = "test"
        image_buffer = qrcode_generator.create_qrcode(data)

        # Assert that the buffer is a valid image
        image = Image.open(io.BytesIO(image_buffer))
        self.assertEqual(image.format, "PNG")

        decoded = qrcode.decode(image)
        self.assertEqual(decoded[0].data.decode("utf-8"), data)


if __name__ == '__main__':
    unittest.main()