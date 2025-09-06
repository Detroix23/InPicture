"""
Given 2 images, find the hidden string.
"""

import numpy
from PIL import Image
from pathlib import Path

import image


class Decode(image.Image):
    def __init__(
        self, 
        origin: str, 
        coded: str, 
        component: int
    ) -> None:
        self.origin: str = origin
        self.coded: str = coded
        self.component: int = component
        

    def compare_images(self) -> list[bool]:
        difference: list[bool] = []
        # Open both files.
        pixels_origin: numpy.ndarray[tuple[int, int, int]]
        pixels_coded: numpy.ndarray[tuple[int, int, int]]
        with Image.open(Path(self.origin_directory + self.origin)) as image_origin:
            pixels_origin = numpy.array(image_origin)
        with Image.open(Path(self.coded_directory + self.coded)) as image_coded:
            pixels_coded = numpy.array(image_coded)

        for row_origin, row_coded in zip(pixels_origin, pixels_coded):
            for origin, coded in zip(row_origin, row_coded):
                if origin[self.component] != coded[self.component]:
                    print(f"diff: {origin} != {coded}")
                    

        return difference

    def read_image_of_text(self, name: str, component: int) -> str:
        ascii_blacklist: list[int] = [0]
        pixels: numpy.ndarray
        with Image.open(Path(self.coded_directory + name)) as image:
            pixels = numpy.array(image)

        message: str = ""
        for row in pixels:
            for pixel in row:
                if pixel[component] not in ascii_blacklist:
                    message += chr(pixel[component])
        
        if not message:
            print("(~) - Message is empty.")
        return message

if __name__ == "__main__":
    import colors
    import test_utils

    print("# TEST - Decode")

    d1 = Decode("medium1.bmp", "medium1.bmp", colors.R)
    #dd1 = d1.compare_images()
    #print(dd1)

    dt1: str = d1.read_image_of_text("message1.bmp", colors.G).strip()
    assert dt1 == test_utils.TEXT_LONG1