"""
Handle, read and decode images
"""

from PIL import Image
import numpy

import binary

class CodedImage:
    directory: str = "./data/"
    coded_directory: str = "./data/coded/"

    def __init__(self, path: str, message: str) -> None:
        self.path: str = path
        self.message: str = message
        self.code_component: int = 0

        self.coded_image: Image.Image = self.code_message_in(self.code_component)
        self.save_image_coded()

    """
    Add to each bit of each the specified component the bit of the coded message
    Component int {0, 1, 2}
    """
    def code_message_in(self, component: int) -> Image.Image:
        coded_image: Image.Image
        with Image.open(self.directory + self.path) as image:
            # Converting image to pixels.
            pixels = numpy.array(image)
            size = (pixels.shape[0], pixels.shape[1])

            # Message to bits
            message_bit: list[bool] = binary.str_to_bin(self.message)

            # Iterating over each pyxel.
            # About overflow: loop around.
            count: int = 0
            for x in range(size[0]):
                for y in range(size[1]):
                    if count < len(message_bit):
                        color_bin = binary.int_to_bin(pixels[x, y][component])
                        color_bin[-1] = message_bit[count]
                        pixels[x, y][component] = binary.bin_to_int(color_bin)
                        count += 1 

            # Generating the coded image.
            coded_image = Image.fromarray(pixels)

        return coded_image

    """
    Save the generated coded image.
    """
    def save_image_coded(self) -> None:
        try:
            self.coded_image.save(self.coded_directory + self.path)
            print(f"(+) - Coded image succesfully saved in `{self.coded_directory + self.path}`.")
        except OSError:
            print(f"(!) - Could not save image in `{self.coded_directory + self.path}`.")

if __name__ == "__main__":
    ci = CodedImage("medium1.bmp", "Hello")