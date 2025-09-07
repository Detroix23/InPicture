"""
Hide a message in a image, in a unoticable way
"""

if __name__ == '__main__':
    import modules.encode as encode
    import modules.decode as decode
    import modules.colors as colors
    import modules.test_utils as test_utils

    print("# InPicture.")
    print("## MAIN.\n")

    print("## ENCODE.")
    ie_mario = encode.Encode(
        "medium1.bmp", 
        test_utils.TEXT_SHORT3, 
        colors.R,
        auto_save=False,
        open_when_ready=True,
    )
    ie_mario.code_message_in()
    ie_mario.save_image_coded()
    
    ie_color1 = encode.Encode(
        "message1.bmp",
        test_utils.TEXT_LONG1,
        colors.G,
        auto_save=True,
        open_when_ready=False,
    )
    ie_color1.create_image_with_text()

    print("## DECODE.")
    d1 = decode.Decode(
        "medium1.bmp", 
        colors.R,
        8,
    )
    dd1: str = d1.read_hidden_text()
    d1.save_decoded_message()

    d2 = decode.Decode(
        "message1.bmp", 
        colors.G,
        8,
    )
    dt2: str = d2.read_image_of_text().strip()
    d2.save_decoded_message()
    assert dt2 == test_utils.TEXT_LONG1