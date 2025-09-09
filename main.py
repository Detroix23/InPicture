"""
Hide a message in a image, in a unoticable way
"""
import modules.encode as encode
import modules.decode as decode
import modules.colors as colors
import modules.test_utils as test_utils
import modules.ui as ui

if __name__ == '__main__':
    print("# InPicture.")
    print("## MAIN.\n")

    print("## ENCODE.")
    ie_mario = encode.Encode(
        "medium1.bmp", 
        test_utils.TEXT_SHORT3, 
        colors.R,
        auto_save=False,
        open_when_ready=False,
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

    ie_moth = encode.Encode(
        "small1.png",
        test_utils.TEXT_SHORT2,
        colors.B,
        auto_save=True,
        open_when_ready=False,
    )
    ie_moth.code_message_in()

    print("## DECODE.")
    d1 = decode.Decode(
        "medium1.bmp", 
        colors.R,
        8,
    )
    d1.read_hidden_text()
    d1.clean_message()
    d1.save_decoded_message()
    assert d1.message_clean == test_utils.TEXT_SHORT3

    d2 = decode.Decode(
        "message1.bmp", 
        colors.G,
        8,
    )
    d2.read_image_of_text()
    d2.clean_message()
    d2.save_decoded_message()
    assert d2.message_clean == test_utils.TEXT_LONG1

    d3 = decode.Decode(
        "small1.png",
        colors.B,
        8,
    )
    d3.read_hidden_text()
    d3.clean_message()
    d3.save_decoded_message()
    assert d3.message_clean == test_utils.TEXT_SHORT2

    print("\n## User interface.\n")
    ui.UiConsole()