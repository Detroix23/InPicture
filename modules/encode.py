"""
Handle, read and decode images
"""

from PIL import Image
import numpy

import image
import binary
import test_utils


class Encode(image.Image):
    """
    Generate from a given origin image a coded image.
    """
    def __init__(self, name: str, message: str, component: int) -> None:
        self.name: str = name
        self.message: str = message
        self.code_component: int = component

        self.coded_image: Image.Image | None = None

    
    def code_message_in(self, component: int) -> Image.Image:
        """
        Modify the origin image by setting the first bit of the color component to the bit of the char string.
        Component int {0, 1, 2}.
        Returns and adds to `coded image` the treated image.
        """
        coded_image: Image.Image
        with Image.open(self.origin_directory + self.name) as image:
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

        self.coded_image = coded_image

        return coded_image

    def create_image_with_text(self, color_mask: tuple[int, int, int]) -> Image.Image:
        """
        Create a monochrome image with the given text.
        Create a square and complete with black pixels.
        Returns and adds to `coded image` the treated image.
        """
        components: int = 3
        # Message to bits
        message_int: numpy.ndarray = numpy.array([ord(letter) for letter in self.message])

        # Fill the 1D array to match the number of pixels needed for the square
        side: int = int(numpy.ceil(numpy.sqrt(len(message_int))))
        while len(message_int) < side ** 2:
            message_int = numpy.insert(message_int, 0, 0, axis=0)
            
        #print("Fs:", message_int)

        # Apply the color mask
        colors: numpy.ndarray = numpy.empty(shape=(message_int.shape + (components,)), dtype='uint8')
        for i, number in enumerate(message_int):
            colors[i] = numpy.array([color_mask[0] * number, color_mask[1] * number, color_mask[2] * number], dtype='uint8')
        
        #print("Cs:", colors)

        # 2D-ify
        square: numpy.ndarray = colors.reshape((side, side, components))

        print("Cc:", square)

        # Convert
        image_from_text: Image.Image = Image.fromarray(square)
        image_from_text.show()
        
        self.coded_image = image_from_text

        return image_from_text


    def save_image_coded(self, custom_name: str | None = None) -> None:
        """
        Save the generated coded image. Optionally, you can give it a custom name (and include the format).
        """
        if self.coded_image is not None:
            name: str
            if custom_name is not None:
                name = custom_name
            else:
                name = self.name

            try:
                self.coded_image.save(self.coded_directory + name)
                print(f"(+) - Coded image succesfully saved in `{self.coded_directory + name}`.")
            except OSError:
                print(f"(!) - Could not save image in `{self.coded_directory + name}`.")
        else:
            print(f"(!) - No image in buffer.")

if __name__ == "__main__":
    import colors
    ie_mario = Encode(
        "medium1.bmp", 
        test_utils.TEXT_LONG1, 
        colors.R
        )
    
    ie_color1 = Encode(
        "message1.bmp",
        test_utils.TEXT_LONG1,
        colors.R
    )
    ie_color1.create_image_with_text((1, 0, 0))
    ie_color1.save_image_coded()