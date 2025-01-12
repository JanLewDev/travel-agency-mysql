"""Modul zawierajacy funkcje pomocnicze."""

import sys
import time


# https://stackoverflow.com/a/34482761
def progressbar(it, prefix="", size=60, out=sys.stdout):
    """Funkcja generujaca pasek postepu."""
    count = len(it)
    start = time.time()  # time estimate start

    def show(j):
        x = int(size * j / count)
        # time estimate calculation and string
        remaining = ((time.time() - start) / j) * (count - j)
        mins, sec = divmod(remaining, 60)  # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        print(
            f"{prefix}[{'█'*x}{('.'*(size-x))}] {j}/{count} Pozostalo {time_str}",
            end="\r",
            file=out,
            flush=True,
        )

    show(0.1)  # avoid div/0
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    print("\n", flush=True, file=out)
