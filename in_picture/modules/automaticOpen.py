"""
Takes in charge the automatic opening of files 
"""

import subprocess 
import os
import platform
import pathlib as path

def open_text(file_path: path.Path) -> None:
    """
    Open text like files automatically using the default text editor/viewer.
    On linux, if you get an error like "symbol loopkup error", it is surely due to the VSCode terminal. 
    Try executing the script on a classic terminal.
    """
    system: str = platform.system()
    try:
        # macOS
        if system == 'Darwin':       
            subprocess.call(('open', file_path))
        # Windows
        elif system == 'Windows':    
            os.startfile(file_path) # type: ignore
        # linux variants
        else:                                   
            subprocess.call(('xdg-open', file_path))
    except OSError as exception:
        print(f"(!) - Can't automatically open the file. Path=`{file_path}`, System=`{system}`, Error=`{exception}`.")

    return

if __name__ == "__main__":
    print("# InPicture.")
    print("## Automatic opening.")

    open_text(path.Path("data/decoded/README.md"))