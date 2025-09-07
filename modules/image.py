"""
Define the most basic image data
"""

class CodeImage:
    """
    Base of a cyphering and decyphering image.
    """
    origin_directory: str = "./data/origin/"
    coded_directory: str = "./data/coded/"
    decoded_directory: str = "./data/decoded/"

    def __init__(self, name: str, message: str, component: int, character_size: int) -> None:
        self.name: str = name
        self.message: str = message
        self.component: int = component
        self.character_size: int = character_size