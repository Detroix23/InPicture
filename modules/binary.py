"""
Image binary computations
"""

"""
def int_to_binary(a: int) -> str:
    bin_a = ""
    #a = a // 2
    if a == 0:
        bin_a = "0"
    else:
        while a > 0:
            bin_a = str(a % 2) + bin_a
            a = a // 2
            #print("a=", a)
    return "2x" + bin_a
"""

"""
Return a binary list containing the digits, in the right to left order.
"""
def int_to_bin(a: int) -> list[bool]:
    bin_a: list[bool] = []
    if a == 0:
        bin_a = [False]
    else:
        while a > 0:
            bin_a.append(bool(a % 2))
            a = a // 2
    bin_a.reverse()
    return bin_a

"""
From a list of binary digits, return an int.
"""
def bin_to_int(bin_digits: list[bool]) -> int:
    number: int = 0
    bin_digits.reverse()
    for index, bit in enumerate(bin_digits):
        number += int(bit) * 2 ** index
    
    return number

"""
Return all digits of all letters of the text in a list.
Case sensitive.
"""
def str_to_bin(text: str) -> list[bool]:
    bin_letters: list[bool] = []
    for letter in text:
        bin_letters = bin_letters + int_to_bin(ord(letter))
    
    return bin_letters

"""
Return a string, ASCII notation, from a list of bits.
Args:
    Letter size to define the number of bits for a letter
    
"""
def bin_to_str(
    bin_letters: str, 
    letter_size: int = 8,
    raise_on_incomplete_char: bool = False
) -> str:
    text: str = ""
    bit_buffer: list[bool] = []
    for bit in bin_letters:
        bit_buffer.append(bit)
        
        if len(bit_buffer) >= letter_size - 1:
            text += chr(bin_to_int(bit_buffer))
            bit_buffer = []


        
    
    if raise_on_incomplete_char and len(bit_buffer):
        raise BufferError(f"(X) - Incomplete char. Buffer is of len {len(bit_buffer)}.") 
    return text

if __name__ == '__main__':
    print("# Binary operations, tests.\n")
    
    b = str_to_bin("ab")
    print("b1", b, len(b))
    
    a = 215684
    a1 = int_to_bin(a)
    a2 = bin_to_int(a1)
    assert a == a2, f"Not eq {a1=} {a2=}"
    
    b2 = str_to_bin("a")
    b2_2 = int_to_bin(97)
    print("b2", b2, b2_2, bin_to_int(b2))
    
    n = bin_to_int([True, True, True, True])
    print(n)
    
    t = bin_to_str(
        [True, True, False, False, False, False, True, True, True, False, False, False, True, False],
        8,
        True
    )
    print(t)
    