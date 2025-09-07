"""
Given 2 images, find the hidden string.
"""

import numpy
from PIL import Image
from pathlib import Path
import datetime


import image
import binary

class Decode(image.Image):
    def __init__(
        self, 
        name: str,  
        component: int,
        character_size: int = 8
    ) -> None:
        self.name: str = name
        self.component: int = component
        self.character_size: int = character_size
        self.message: str = ""

    def read_hidden_text(self) -> str:
        bits: numpy.ndarray = numpy.array([], dtype=bool)
        # Open both files.
        pixels: numpy.ndarray[tuple[int, int, int]]
        with Image.open(Path(self.coded_directory + self.name)) as image:
            pixels = numpy.array(image)

        # Get for each pixel the first bit of the color component.
        for row in pixels:
            for pixel in row:
                first_bit: bool = binary.int_to_bin(pixel[self.component])[-1]
                #print(first_bit, end=" ")
                bits = numpy.append(bits, first_bit)

        #print(f"Bin: {bits[0:48]}")
        # Get character chain
        decoded_str: str = binary.bin_to_str(bits, self.character_size, False)

        self.message = decoded_str

        return decoded_str

    def read_image_of_text(self, custom_component: int | None = None) -> str:
        component: int
        if custom_component is not None:
            component = custom_component
        else:
            component = self.component

        ascii_blacklist: list[int] = [0]
        # All pixels of image
        pixels: numpy.ndarray
        with Image.open(Path(self.coded_directory + self.name)) as image:
            pixels = numpy.array(image)

        message: str = ""
        for row in pixels:
            for pixel in row:
                if pixel[component] not in ascii_blacklist:
                    message += chr(pixel[component])
        
        if not message:
            print("(~) - Message is empty.")

        self.message = message
        
        return message

    def save_decoded_message(self, custom_name: str | None = None) -> None:
        name: str
        if custom_name is None:
            name = self.name
        else:
            name = custom_name
        
        try:
            with open(Path(self.decoded_directory + name + ".log"), "a") as file_save:
                file_save.write(f"Decoding {self.decoded_directory + name}, on {datetime.datetime.now()}.\n")
                file_save.write("Raw: \n")
                file_save.write(self.message)
                file_save.write("\n\nEND.\n\n")
            print(f"(+) - Succesfully saved in `{self.decoded_directory + name}.log`.")
        except OSError:
            print(f"(!) - Couldn't log in `{self.decoded_directory + name}.log`.")

if __name__ == "__main__":
    import colors
    import test_utils

    print("# InPicture.")
    print("## DECODE.")

    d1 = Decode(
        "medium1.bmp", 
        colors.R,
        8,
    )
    dd1: str = d1.read_hidden_text()
    d1.save_decoded_message()

    d2 = Decode(
        "message1.bmp", 
        colors.G,
        8,
    )
    dt2: str = d2.read_image_of_text().strip()
    d2.save_decoded_message()
    assert dt2 == test_utils.TEXT_LONG1