from time import sleep, perf_counter
from itertools import count

class Clock:
    """
    When run, ticks at a constant rate. Each tick yields an incrementing integer.

        c = Clock()
        for tick in c.run():
            print(tick)
    """
    def __init__(self, interval=0.1):
        self.interval = interval

    def run(self):
        previous_tick = perf_counter()
        error = 0
        for i in count():
            yield i
            sleep(max(self.interval - error, 0))
            latest_tick = perf_counter()
            error = latest_tick - previous_tick - self.interval
            previous_tick = latest_tick
