"""
IN PICTURE
loadings.py
Aim: loading bars and spinners like `alive_progress`, `tqdm`,...
Utilize the \r escape operator
"""

import time

class Bar:
    _i: int
    progress_bar_symbol: str
    
    def __init__(self, progress: str, prefix: str, max_iterations: int, *, true_size: int = 0, empty: str = "░", borders: str = "|") -> None:
        self._i = 0
        self.first_time: float = 0

        self.max: int = max_iterations if max_iterations > 0 else 1
        
        self.progress_bar_symbol: str = progress
        self.progress_bar_empty: str = empty
        self.borders: str = borders
        self.prefix: str = prefix
        self.suffix: str = " "
        self.true_size: int = true_size
        
    def reset(self) -> None:
        """
        Reset the counter. Run this method when using default bars.
        """
        self._i = 0
        self.first_time: float = 0

    def increment(self) -> None:
        if self.first_time == 0:
            self.first_time = time.monotonic()
        
        self._i += 1
        bar: str
        if self.true_size > 0 and self._i <= self.max:
            true_i: int = int(self.true_size * (float(self._i) / float(self.max)))
            bar = (
                self.progress_bar_symbol * true_i
                + self.progress_bar_empty * (self.true_size - true_i)
            )
        elif self.true_size > 0 and self._i > self.max:
            bar = self.progress_bar_symbol * self.true_size 
        elif self._i <= self.max:
            bar = (
                self.progress_bar_symbol * self._i
                + self.progress_bar_empty * (self.max - self._i)
            )
        else:
            bar = self.progress_bar_symbol * self.max

        template: str = "\r"

        template += self.prefix
        template += self.borders
        template += bar
        template += self.borders
        template += " - "

        percentage: float = self._i / self.max * 100
        template += f"{percentage:.1f}% "
        template += f"{self._i}/{self.max}ops "

        time_elapsed: float = time.monotonic() - self.first_time
        template += f"{time_elapsed:.2f}s "

        template += self.suffix

        print(
            template,
            end="\r"
        )
        
class Spinner:
    _i: int
    progress_bar_symbol: str
    
    def __init__(self, symbols: list[str] | str, max: int = 0, *, span: int = 1, multiple: int = 1) -> None:
        self._i = 0
        self.first_time: float = 0

        self.max: int = max
        self.multiple: int = multiple
        
        self.symbols: list[str] | str = symbols
        self.borders: str = "|"
        self.prefix: str = "Loading: "
        self.suffix: str = " "
        self.span: int = span
        
    
    def reset(self) -> None:
        """
        Reset the counter. Run this method when using default bars.
        """
        self._i = 0
        self.first_time: float = 0


    def increment(self) -> None:
        """
        Progress the bar for 1 tick.
        """
        if self.first_time == 0:
            self.first_time = time.monotonic()
        
        self._i += 1
        i: int = self._i // self.multiple
        
        

        spinner: str = ""
        for j in range(self.span):
            spinner += self.symbols[(i + j) % len(self.symbols)]
        
        template: str = "\r"

        template += self.prefix
        template += self.borders
        template += spinner
        template += self.borders
        template += " - "

        if self.max != 0:
            percentage: float = self._i / self.max * 100
            template += f"{percentage:.1f}% "
            template += f"{self._i}/{self.max}ops "
        else:
            template += f"{self._i}ops "

        time_elapsed: float = time.monotonic() - self.first_time
        template += f"{time_elapsed:.2f}s "

        template += self.suffix

        print(
            template,
            end="\r"
        )
        

        
# Default
bar: dict[str, Bar] = {
    "SimpleFull1": Bar(
        "█",
        "Loading: ",
        100,
        true_size=10    
    ),
}
spinner: dict[str, Spinner] = {
    "Bars1": Spinner(
        ["│", "╲", "─", "/"],
        max=1000,
        multiple=2,
    ),
    "Wave1": Spinner(
        ["▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂", "▁"],
        span=3,
        multiple=1
    ),
    "Wave2": Spinner(
        ["▂", "▄", "▆", "█", "▆", "▄", "▂", "▁"],
        span=3,
        multiple=1
    ),
    # Box-drawing chars: ▖▗▘▙▚▛▜▝▞▟
    "Solid1": Spinner(
        "▙▚▘▛▞▝▜▚▗▟▞▖"
    ),
    "Solid2": Spinner(
        "▙▌▛▔▜▐▟▁"
    ),
}


if __name__ == "__main__":
    
    for _ in range(200):
        bar["SimpleFull1"].increment()
        # spinner["Bars1"].increment()
        time.sleep(0.1)

    print()    