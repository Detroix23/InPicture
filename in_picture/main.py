"""
Hide a message in a image, in a unoticable way
"""
import modules.ui as ui

def main() -> None:
    print(ui.TEXT["Title"])
    print(ui.TEXT["Main"])

    ui.UiConsole()
    print(ui.TEXT["End"])

if __name__ == '__main__':
    main()