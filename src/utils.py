import os

from rich.panel import Panel
from rich.align import Align

ASCII_ART: str = """
                ~~ E-LEARNING PLATFORM ~~

         .'----------`.                              
         | .--------. |                             
         | |########| |       __________              
         | |########| |      /__________\\             
.--------| `--------' |------|    --=-- |-------------.
|        `----,-.-----'      |o ======  |             | 
|       ______|_|_______     |__________|             | 
|      /  %%%%%%%%%%%%  \\                             | 
|     /  %%%%%%%%%%%%%%  \\                            | 
|     ^^^^^^^^^^^^^^^^^^^^                            | 
+-----------------------------------------------------+
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
"""


def clear_screen() -> None:
    """Clears the terminal screen for both Windows and Linux."""

    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

    return None


def header(title: str) -> Panel:
    return Panel(Align.center(ASCII_ART),
                 title=title, style="cyan")
