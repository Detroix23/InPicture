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
        self.coded_image: Image = self.code_message_in(self.code_component)

    """
    Add to each bit of each the specified component the bit of the coded message
    Component int {0, 1, 2}
    """
    def code_message_in(self, component: int) -> Image:
        coded_image: Image
        with Image.open(self.directory + self.path) as image:
            # Converting image to pixels.
            pixels = numpy.array(image)
            size = (pixels.shape[0], pixels.shape[1])
            print(pixels.dtype, size)

            l = [bool(i) for i in [0, 1, 1, 1, 0]]
            # Iterating over each pyxel.
            # About overflow: loop around.
            count: int = 0
            for x in range(size[0]):
                for y in range(size[1]):
                    if count < len(l):
                        #print("Cp:", pixels[x, y][component], end=" ")
                        color_bin = binary.int_to_bin(pixels[x, y][component])
                        color_bin[-1] = l[count]
                        pixels[x, y][component] = binary.bin_to_int(color_bin)
                        #print("Cp:", pixels[x, y][component])
                        count += 1 

            # Generating and saving coded image.
            coded_image = Image.fromarray(pixels)
            coded_image.save(self.coded_directory + self.path)

        if coded_image is None:
            raise Error(f"(X) - Coded image is None.")
        return coded_image

if __name__ == "__main__":
    ci = CodedImage("medium1.bmp", "Hello")
