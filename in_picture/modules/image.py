"""
Define the most basic image data
"""
import pathlib as path

class CodeImage:
    """
    Base of a cyphering and decyphering image.
    """
    origin_directory: path.Path = path.Path("./data/origin/")
    coded_directory: path.Path = path.Path("./data/coded/")
    decoded_directory: path.Path = path.Path("./data/decoded/")

    def __init__(self, name: str, message: str, component: int, character_size: int) -> None:
        self.name: str = name
        self.message: str = message
        self.component: int = component
        self.character_size: int = character_size

        self.time_elapsed: float = 0
