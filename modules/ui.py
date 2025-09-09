import modules.encode as encode
import modules.decode as decode

class UiConsole:
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

    @staticmethod
    def verfied_input(
        message: str,
        symbols: dict[str, list[str]] | None = None,
        default: int | None = None,
        must_validate: bool = True,
        allowed_type: type = str,
        error_message: str = "(!) - Incorrect input. Please try again.",
        max_iterations: int = 10000,
    ) -> str:
        """
        A genral use input sanitaizer that repeats until the user has entered a correct value.
        `Allowed` contains as keys the true machine return symbol and as value the list of all string that corrispond to that key.
        If none, all responses are correct.
        `Default` is the index of the default key of the allowed list.
        """
        valid: bool = False
        true_response: str | None = None 
        i: int = 0
        while not valid and i < max_iterations:
            response: str = input(message)
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


    def main_loop(self) -> None:
        try:
            while self.is_running:
                # Choosing side.
                print("## Enter values. [allowed values] (default value). Ctrl+C to exit at any time.")
                action_mode: str = UiConsole.verfied_input(
                    "- Choose an action, a mode [encode, en | decode, de](en): ",
                    self.symbol_mode,
                    default=0
                )
                match action_mode:
                    case "en":
                        print("### Encoding.")
                        name: str = UiConsole.verfied_input("- Name of the file to be encoded [str]: ")
                        message: str = UiConsole.verfied_input("- Message [str]: ")
                        color: int = int(UiConsole.verfied_input(
                            "- Color component, RGB [0 | 1 | 2](0): ", 
                            self.symbol_component, 
                            default=0,
                        ))
                        open_when_ready: bool = bool(UiConsole.verfied_input(
                            "- Open when ready [Yes/ No](Yes): ",
                            self.symbol_bool,
                            default=1
                        ))

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
                            save: bool = bool(UiConsole.verfied_input(
                                "- Save [Yes/ No](Yes): ",
                                self.symbol_bool,
                                default=1    
                            ))
                            if save:
                                image_encode.save_image_coded()
                            else:
                                print("*Canceling.*")
                        else:
                            image_encode.save_image_coded()


                    case "de":
                        print("### Decoding.")
                        name: str = UiConsole.verfied_input("- Name of the file to decode [str]: ")
                        color: int = int(UiConsole.verfied_input(
                            "- Color component RGB [0 | 1 | 2](0): ",
                            self.symbol_component,
                            default=0,
                        ))
                        character_size: int = 8
                        open_when_ready: bool = True
                        log_raw: bool = False

                        image_decode: decode.Decode = decode.Decode(
                            name,
                            color,
                            character_size,
                            open_when_ready=open_when_ready,
                            log_raw=log_raw,
                        )
                        image_decode.read_hidden_text()

                    case _:
                        print("(X) - Invalid mode.")
                    
        except KeyboardInterrupt as exception:
            print(f"\n*Interrupted the main loop `{exception}`. Executing the UI.*\n")
        
        return
                

if __name__ == "__main__":
    print("# InPicture.")
    print("## UI.")

    u = UiConsole()
