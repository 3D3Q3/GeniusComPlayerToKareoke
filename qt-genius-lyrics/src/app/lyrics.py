from typing import List, Tuple, Optional


class Lyrics:
    """Lightweight lyrics/timing helper used by tests and the app.

    Expectations from tests:
    - set_timing_data(list_of_(time, text))
    - get_current_line(current_time) -> Optional[str]
    - get_line_at_time(time) -> Optional[str]
    """

    def __init__(self):
        self.timing: List[Tuple[float, str]] = []

    def set_timing_data(self, timing: List[Tuple[float, str]]) -> None:
        # Expect a list of (time_in_seconds, text)
        self.timing = sorted([(float(t), str(text)) for t, text in timing], key=lambda x: x[0])

    def get_line_at_time(self, time: float) -> Optional[str]:
        # Return the exact line that starts at 'time' if present, else None
        for t, text in self.timing:
            if int(t) == int(time):
                return text
        return None

    def get_current_line(self, current_time: float) -> Optional[str]:
        # Return the latest line whose timestamp is <= current_time.
        if not self.timing:
            return None
        last = None
        for t, text in self.timing:
            if current_time < t:
                break
            last = text
        return last
