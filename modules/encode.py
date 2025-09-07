"""
Handle, read and decode images
"""

from PIL import Image
import numpy

import modules.image as image
import modules.binary as binary

# Bloated typing for decorator.
from typing import Callable, ParamSpec
Param = ParamSpec("Param")
def processing(function: Callable[..., tuple[Image.Image, numpy.ndarray]]) -> Callable[..., Image.Image]:
    """
    Allow common task after and before the processing of an image.
    """
    def wrapper(self: 'Encode', *args: Param.args, **kwargs: Param.kwargs) -> Image.Image:
        image, pixels = function(self, *args, **kwargs)
        if self.print_array:
            print(f"Pixels of image `{self.name}`: {pixels}")
        if self.open_when_ready and self.coded_image is not None:
            print(f"Displaying image `{self.name}`.")
            self.coded_image.show()
        if self.auto_save:
            self.save_image_coded()


        return image
    return wrapper

class Encode(image.CodeImage):
    """
    Generate from a given origin image a coded image.
    """
    def __init__(
        self, 
        name: str, 
        message: str, 
        component: int,
        character_size: int = 8,
        auto_save: bool = False,
        open_when_ready: bool = True,
        print_array: bool = False
    ) -> None:
        super().__init__(
            name, 
            message, 
            component,
            character_size
        ) 

        self.auto_save: bool = auto_save
        self.open_when_ready: bool = open_when_ready
        self.print_array: bool = print_array

        self.coded_image: Image.Image | None = None

    
    @processing
    def code_message_in(self, custom_component: int | None = None) -> tuple[Image.Image, numpy.ndarray]:
        """
        Modify the origin image by setting the first bit of the color component to the bit of the char string.
        Component int {0, 1, 2}.
        Returns and adds to `coded image` the treated image.
        """
        # Colors
        component: int
        if custom_component is None:
            component = self.component
        else:
            component = custom_component

        # Loading image
        pixels: numpy.ndarray
        coded_image: Image.Image
        # Converting image to pixels.
        with Image.open(self.origin_directory + self.name) as image:
            pixels = numpy.array(image)
        size: tuple[int, int] = (pixels.shape[0], pixels.shape[1])

        # Message to bits
        message_bit: list[bool] = binary.str_to_bin(self.message, self.character_size)
        #print(f"Bin: {message_bit[0:48]}")

        # Iterating over each pyxel.
        # About overflow: loop around.
        count: int = 0
        for x in range(size[0]):
            for y in range(size[1]):
                if count < len(message_bit):
                    #print(message_bit[count], end=" ")
                    color_bin = binary.int_to_bin(pixels[x, y][component], self.character_size)
                    color_bin[-1] = message_bit[count]
                    pixels[x, y, component] = binary.bin_to_int(color_bin)
                    count += 1 

        # Generating the coded image.
        coded_image = Image.fromarray(pixels)

        self.coded_image = coded_image

        return coded_image, pixels

    @processing
    def create_image_with_text(self, custom_color_mask: tuple[int, int, int] | None = None) -> tuple[Image.Image, numpy.ndarray]:
        """
        Create a monochrome image with the given text.
        Create a square and complete with black pixels.
        Returns and adds to `coded image` the treated image.
        """
        # Colors
        color_mask: tuple[int, int, int]
        if custom_color_mask is None:
            color_mask_temp = [0, 0, 0]
            color_mask_temp[self.component] = 1
            color_mask = tuple(color_mask_temp)  # type: ignore[reportAssignmentType]
        else:
            color_mask = custom_color_mask

        components: int = len(color_mask)


        # Message to bits (wipes character that are bigger than 255).
        message_int: numpy.ndarray = numpy.array([ord(letter) for letter in self.message if ord(letter) < 256])

        # Fill the 1D array to match the number of pixels needed for the square
        side: int = int(numpy.ceil(numpy.sqrt(len(message_int))))
        while len(message_int) < side ** 2:
            message_int = numpy.insert(message_int, 0, 0, axis=0)

        # Apply the color mask
        colors: numpy.ndarray = numpy.empty(
            shape=(message_int.shape + (components,)), 
            dtype="uint8"
        )
        for i, number in enumerate(message_int):
            colors[i] = numpy.array(
                [color_mask[0] * number, color_mask[1] * number, color_mask[2] * number], 
                dtype="uint8"
            )
        
        # 2D-ify
        square: numpy.ndarray = colors.reshape((side, side, components))

        # Convert
        image_from_text: Image.Image = Image.fromarray(square)
        
        self.coded_image = image_from_text

        return image_from_text, square


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
    import test_utils

    print("# InPicture.")
    print("## ENCODE.")


    ie_mario = Encode(
        "medium1.bmp", 
        test_utils.TEXT_SHORT1, 
        colors.R,
        auto_save=False,
        open_when_ready=True,
    )
    ie_mario.code_message_in()
    ie_mario.save_image_coded()
    
    ie_color1 = Encode(
        "message1.bmp",
        test_utils.TEXT_LONG1,
        colors.G,
        auto_save=True,
        open_when_ready=False,
    )
    ie_color1.create_image_with_text()