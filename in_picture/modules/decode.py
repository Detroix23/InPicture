"""
Find the hidden string from an image.
"""

import numpy
from PIL import Image
from pathlib import Path
import datetime
import time


import modules.image as image
import modules.binary as binary
import modules.automaticOpen as autoOpen

# Bloated typing for decorator.
from typing import Callable, ParamSpec
Param = ParamSpec("Param")
def processing(function: Callable[..., str]) -> Callable[..., str]:
    """
    Allow common task after and before the processing of an image.
    """
    def wrapper(self: 'Decode', *args: Param.args, **kwargs: Param.kwargs) -> str:
        message: str = function(self, *args, **kwargs)
        if self.open_when_ready and self.message:
            print(f"Opening, using default text editor, `{self.decoded_directory}{self.name}`.")
            autoOpen.open_text(self.decoded_directory / (self.name + ".log"))
        if self.do_clean and message:
            self.clean_message()
        if self.save:
            self.save_decoded_message()
        return message
    return wrapper

class Decode(image.CodeImage):
    def __init__(
        self, 
        name: str,  
        component: int,
        character_size: int = 8,
        open_when_ready: bool = True,
        log_raw: bool = False,
        save: bool = True,

    ) -> None:
        super().__init__(
            name, 
            "", 
            component,
            character_size
        ) 

        self.character_size: int = character_size
        self.message_clean: str = ""

        self.do_clean: bool = True
        self.log_raw: bool = log_raw
        self.open_when_ready: bool = open_when_ready
        self.save: bool = save

    @processing
    def read_hidden_text(self) -> str:
        bits: numpy.ndarray = numpy.array([], dtype=bool)
        # Open both files.
        pixels: numpy.ndarray[tuple[int, int, int]]
        image_path: Path = self.coded_directory / self.name
        with Image.open(image_path) as image:
            pixels = numpy.array(image)

        # Get for each pixel the first bit of the color component.
        time_start: float = time.monotonic()
        for row in pixels:
            for pixel in row:
                first_bit: bool = binary.int_to_bin(pixel[self.component])[-1]
                #print(first_bit, end=" ")
                bits = numpy.append(bits, first_bit)

        #print(f"Bin: {bits[0:48]}")
        # Get character chain
        decoded_str: str = binary.bin_to_str(bits, self.character_size, False)
        self.time_elapsed = time.monotonic() - time_start

        self.message = decoded_str

        return decoded_str

    @processing
    def read_image_of_text(self, custom_component: int | None = None) -> str:
        component: int
        if custom_component is not None:
            component = custom_component
        else:
            component = self.component

        ascii_blacklist: list[int] = [0]

        # All pixels of image
        time_start: float = time.monotonic()
        pixels: numpy.ndarray
        image_path: Path = self.coded_directory / self.name
        with Image.open(image_path) as image:
            pixels = numpy.array(image)

        message: str = ""
        for row in pixels:
            for pixel in row:
                if pixel[component] not in ascii_blacklist:
                    message += chr(pixel[component])
        self.time_elapsed = time.monotonic() - time_start
        

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
        log_path: Path = self.decoded_directory / (name + ".log")
        image_path: Path = self.decoded_directory / name

        try:
            with open(log_path, "a") as file_save:
                file_save.write(f"Decoding {image_path}, on {datetime.datetime.now()}.\n")
                file_save.write(f"Color component: {self.component}. Decipher time: {self.time_elapsed:.8f}s.\n")
                if self.message and self.log_raw:
                    file_save.write("Raw: \n")
                    file_save.write(f"{self.message}\n")
                elif self.log_raw:
                    file_save.write("No raw message.\n")
                if self.message_clean:
                    file_save.write("Clean: \n")
                    file_save.write(f"{self.message_clean}\n")
                elif not self.log_raw:
                    file_save.write("No messsage.\n")

                file_save.write("\nEND.\n\n")
            print(f"(+) - Succesfully saved in `{log_path}`. Decoded in {self.time_elapsed:.4f}s.")
        except OSError:
            print(f"(!) - Couldn't log in `{log_path}`.")

    def clean_message(self) -> str:
        """
        Clean the decoded message by: triming, watching for key word "STOP.", and consecutive non-alphanumeric characters.
        """
        alphanumerics: list[str] = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ',', '.', '!', '?', ';', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
        alphanumeric_checks: int = 3
        stop_symbol: str = "STOP."
        # Triming
        clean_message: str = self.message.strip()
        # STOP.
        stop_index: int = clean_message.find(stop_symbol)
        if stop_index != -1:
            clean_message = clean_message[0: stop_index + len(stop_symbol) + 1]
        # Consecutive chars
        i: int = 0
        alphanumeric_valid: bool = True
        while alphanumeric_valid and i < len(clean_message):
            local_valid: bool = False
            j: int = 0
            while not local_valid and j < alphanumeric_checks and i + j < len(clean_message):
                # On the whole checks, if one is a valid alphanumerical, the whole test is correct.
                local_valid |= clean_message[i + j] in alphanumerics
                j += 1
            # If true, remains true, else false.
            alphanumeric_valid &= local_valid
            i += 1
        if not alphanumeric_valid:
            clean_message = clean_message[0: i - 1]

        #print(clean_message)
        self.message_clean = clean_message

        return clean_message


if __name__ == "__main__":
    import colors
    import modules.testUtils as testUtils

    print("# InPicture.")
    print("## DECODE.")

    d1 = Decode(
        "medium1.bmp", 
        colors.R,
        8,
    )
    dd1: str = d1.read_hidden_text()
    d1.clean_message()
    d1.save_decoded_message()

    d2 = Decode(
        "message1.bmp", 
        colors.G,
        8,
    )
    dt2: str = d2.read_image_of_text().strip()
    d2.clean_message()
    d2.save_decoded_message()
    assert dt2 == testUtils.TEXT_LONG1