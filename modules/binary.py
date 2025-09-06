"""
Image binary computations
"""
import numpy

"""
Return a binary list containing the digits, in the right to left order.
Encoding of bit size `size`.
"""
def int_to_bin(a: int, size: int = 8) -> list[bool]:
    bin_a: list[bool] = []
    if a == 0:
        bin_a = [False]
    else:
        while size > 0:
            bin_a.append(bool(a % 2))
            a = a // 2
            size -= 1
    bin_a.reverse()
    return bin_a

"""
Return all digits of all letters of the text in a list.
Case sensitive.
"""
def str_to_bin(text: str, size: int = 8) -> list[bool]:
    bin_letters: list[bool] = []
    for letter in text:
        bin_letters = bin_letters + int_to_bin(ord(letter), size)
    
    return bin_letters

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
Return a string, ASCII notation, from a list of bits.
Args:
    Letter size to define the number of bits for a letter
    
"""
def bin_to_str(
    bin_letters: list[bool] | numpy.ndarray, 
    letter_size: int = 8,
    raise_on_incomplete_char: bool = False
) -> str:
    text: str = ""
    bit_buffer: list[bool] = []
    cnt: int = 0
    for bit in bin_letters:
        bit_buffer.append(bit)
        
        if len(bit_buffer) >= letter_size:
            ascii_number: int = bin_to_int(bit_buffer)
            text += chr(ascii_number)
            bit_buffer = []
        cnt += 1

    if raise_on_incomplete_char and len(bit_buffer):
        raise BufferError(f"(X) - Incomplete char. Buffer is of len {len(bit_buffer)}.") 
    elif len(bit_buffer):
        text += chr(bin_to_int(bit_buffer))

    #print(f"bin_to_str: return: {text}")
    return text


if __name__ == '__main__':
    print("# Binary operations, tests.\n")
    
    b1: list[bool] = str_to_bin("ab")
    # print("b1", b, len(b))
    
    a = 254
    a1 = int_to_bin(a)
    # print("a1", a1)
    a2 = bin_to_int(a1)
    assert a == a2, f"Not eq {a1=} {a2=}"
    
    b2: str = "a"
    b2_b = str_to_bin(b2)
    b2_1 = bin_to_str(b2_b)
    b2_2 = int_to_bin(97)
    print("b2", b2, "str:", b2_1, "bin: ", b2_2, bin_to_int(b2_b))
    
    n = bin_to_int([True, True, True, True])
    print(n)
    
    t = bin_to_str(
        [False, True, True, False, False, False, False, True, False, True, True, False, False, False, True, False],
        8,
        True
    )
    print(t)
    