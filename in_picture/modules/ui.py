"""
UI Controller of InPicture.
UiConsole allow the user to use an interactive terminal console.
"""

import pathlib as path
import os

import modules.image as image
import modules.encode as encode
import modules.decode as decode

class UiConsole(image.CodeImage):
    """
    Allow user to type in instructions in the command line. 
    """
    symbol_mode: dict[str, list[str]] = {
        "en": ["en", "encode", "enc"],
        "de": ["de", "decode", "dec"]
    }
    symbol_component: dict[str, list[str]] = {
        "0": ["R", "red", "0"], 
        "1": ["G", "green", "1"],
        "2": ["B", "blue", "2"]
    }
    symbol_bool: dict[str, list[str]] = {
        "0": ["No", "NO", "no", "n", "N"],
        "1": ["Yes", "YES", "yes", "ye", "y", "Y"]
    }

    def __init__(self, debug: bool = False) -> None:
        self.is_running: bool = True
        self.debug: bool = debug

        if self.debug:
            print("!Entering interactive mode. [availble](default).")
        self.main_loop()

    def main_loop(self) -> None:
        try:
            while self.is_running:
                # Choosing side.
                print("\n## Enter values. [allowed values] (default value). Ctrl+C to exit at any time.\n")
                action_mode: str = UiConsole.verfied_input(
                    "- Choose an action, a mode [encode, en | decode, de](en): ",
                    self.symbol_mode,
                    default=0
                )
                if action_mode == "en":
                    print("### Encoding.")
                    self.list_directory(self.origin_directory)

                    name: str = UiConsole.verfied_input(
                        "- Name of the file to be encoded [str]: ",
                        symbols=list(os.listdir(self.coded_directory)),
                        error_message="(!) - File not in directory.",
                    )
                    message: str = UiConsole.verfied_input("- Message [str]: ")
                    color: int = int(UiConsole.verfied_input(
                        "- Color component, RGB [0 | 1 | 2](0): ", 
                        self.symbol_component, 
                        default=0,
                    ))
                    open_when_ready: bool = UiConsole.boolean_input(
                        "- Open when ready [Yes/ No](Yes): ",
                        default=True
                    )

                    image_encode: encode.Encode = encode.Encode(
                        name,
                        message,
                        color,
                        auto_save=False,
                        open_when_ready=open_when_ready,
                        print_array=self.debug
                    )
                    image_encode.code_message_in()

                    if open_when_ready:
                        save: bool = UiConsole.boolean_input(
                            "- Save [Yes/ No](Yes): ",
                            default=True,
                        )
                        if save:
                            image_encode.save_image_coded()
                        else:
                            print("*Canceling.*")
                    else:
                        image_encode.save_image_coded()

                elif action_mode == "de":
                    print("### Decoding.")
                    self.list_directory(self.coded_directory)

                    name: str = UiConsole.verfied_input(
                        "- Name of the file to decode [str]: ",
                        symbols=list(os.listdir(self.coded_directory)),
                        error_message="(!) - File not in directory.",
                    )
                    color: int = int(UiConsole.verfied_input(
                        "- Color component RGB [0 | 1 | 2](0): ",
                        self.symbol_component,
                        default=0,
                    ))
                    character_size: int = 8
                    open_when_ready: bool = True
                    log_raw: bool = False
                    save: bool = True

                    image_decode: decode.Decode = decode.Decode(
                        name,
                        color,
                        character_size,
                        open_when_ready=open_when_ready,
                        log_raw=log_raw,
                        save=save,
                    )
                    image_decode.read_hidden_text()
                    
        except KeyboardInterrupt as exception:
            print(f"\n*Interrupted the main loop `{exception}`. Executing the UI.*\n")
        
        return

    @staticmethod
    def list_directory(directory: path.Path) -> None:
        """
        Print the items of the given directory
        """
        print(f"*Files in `{directory}`.*")
        files: list[str] = os.listdir(directory)

        for file in files:
            if file.lower() not in ["readme.md", "readme"]:
                print(f"\t- {file}")
        print()
        return

    @staticmethod
    def verfied_input(
        message: str,
        symbols: dict[str, list[str]] | list[str] | None = None,
        default: int | None = None,
        must_validate: bool = True,
        allowed_type: type = str,
        error_message: str = "(!) - Incorrect input. Please try again.",
        max_iterations: int = 10000,
    ) -> str:
        """
        A genral use input sanitaizer that repeats until the user has entered a correct value.
        `Symbols` define the allowed keywords that the user can type. 
            - None (default): no restriction
            - list[str]: Only one keyword for each symbol, itself
            - dict[str, list[str]]: Each symbol can have multiple keywords.
        `Allowed` contains as keys the true machine return symbol and as value the list of all string that corrispond to that key.
        If none, all responses are correct.
        `Default` is the index of the default key of the allowed list.
        """
        valid: bool = False
        true_response: str | None = None 
        i: int = 0
        if isinstance(symbols, list):
            symbols = {symbol: [symbol] for symbol in symbols}

        while not valid and i < max_iterations:
            response: str = input(message).strip()

            if response == "" and default is None:
                pass
            elif symbols is None:
                try:
                    allowed_type(response)
                except:
                    pass
                else:
                    true_response = response
                    valid = True
            elif response == "":
                if default is not None:
                    true_response = list(symbols.keys())[default]
                    valid = True
            else:
                for key, values in symbols.items():
                    if response in values:
                        try:
                            allowed_type(response)
                        except:
                            pass
                        else:
                            true_response = key
                            valid = True
            if not valid:
                print(f"{error_message}({response}). ", end="\n")
            i += 1

        if not valid or true_response is None:
            raise ValueError(f"(X) - Can't return an invalid response.")
        print(f"R: `{true_response}`")
        return true_response

    @staticmethod
    def boolean_input(
        message: str,
        default: bool = True, 
        error_message: str = "(!) - Incorrect input. Please try again.",
        max_iterations: int = 10000,
    ) -> bool:
        """
        A boolean (yes/ no) input sanitaizer that repeats until the user has entered a correct value.
        `Default` is the value returned in case the user just presses Enter.
        """
        valid: bool = False
        true_response: bool | None = None 
        i: int = 0
        symbols: dict[bool, list[str]] = {
            False: ["No", "NO", "no", "n", "N"],
            True: ["Yes", "YES", "yes", "ye", "y", "Y"]
        }

        while not valid and i < max_iterations:
            response: str = input(message).strip()

            if response == "":
                true_response = default
                valid = True
            else:
                for key, values in symbols.items():
                    if response in values:
                        true_response = key
                        valid = True
            if not valid:
                print(f"{error_message}({response}). ", end="\n")
            i += 1

        if not valid or true_response is None:
            raise ValueError(f"(X) - Can't return an invalid response.")
        print(f"R: `{true_response}`")
        return true_response

      

