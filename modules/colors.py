"""
Define colors.
"""

"""
Define a RGB color based on 255 resolution.
"""
class ColorRGB:
    def __init__(self, r: int, g: int, b: int) -> None:
        self.r: int = r
        self.g: int = g
        self.b: int = b
        
    def __str__(self) -> str:
        return f"{self.r}, {self.g}, {self.b}"
    
    def __repr__(self) -> str:
        return f"ColorRGB: r={self.r}, g={self.g}, b={self.b}: "
        
if __name__ == "__main__":
    c = ColorRGB(123, 323, 0)
    print("Color", c)