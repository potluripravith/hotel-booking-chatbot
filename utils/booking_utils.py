from datetime import datetime, timedelta
import parsedatetime as pdt
import pandas as pd
from typing import List, Callable
import os

import re
def load_room_data() -> pd.DataFrame:
    """
    Loads the room availability data from a CSV file
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, '..', 'knowledge_base', 'Hotel_availability.csv')
    return pd.read_csv(path)

import parsedatetime as pdt
from datetime import datetime, timedelta
from typing import List, Callable
import re

def normalize_date(input_str: str, base_date: datetime) -> List[str]:
    cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
    text = input_str.strip().lower()

    def format_range(start: datetime, end: datetime) -> List[str]:
        return [
            (start + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end - start).days + 1)
        ]

    def get_week_start(offset_weeks: int = 0) -> datetime:
        """Return the Monday of the current or future week"""
        monday = base_date - timedelta(days=base_date.weekday())  # this week's Monday
        return monday + timedelta(weeks=offset_weeks)

    def get_week(offset_weeks: int = 0) -> List[str]:
        monday = get_week_start(offset_weeks)
        return format_range(monday, monday + timedelta(days=6))

    def get_weekend(offset_weeks: int = 0) -> List[str]:
        saturday = get_week_start(offset_weeks) + timedelta(days=5)
        sunday = saturday + timedelta(days=1)
        return [saturday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")]

    def parse_next_n_days(n: int) -> List[str]:
        return [(base_date + timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(n)]

    def parse_month_day_range(m: re.Match) -> List[str]:
        start_part, day_end, year = m.groups()
        month = start_part.split()[0]
        day_start = start_part.split()[1]
        start = cal.parseDT(f"{month} {day_start}, {year}", base_date)[0].date()
        end = cal.parseDT(f"{month} {day_end}, {year}", base_date)[0].date()
        return format_range(start, end)

    # Literal expressions
    literals: dict[str, Callable[[], List[str]]] = {
        "this weekend": lambda: get_weekend(0),
        "weekend": lambda: get_weekend(0),
        "next weekend": lambda: get_weekend(1),
        "this week": lambda: get_week(0),
        "next week": lambda: get_week(1),
    }

    if text in literals:
        return literals[text]()

    # Regex-based rules
    pattern_handlers: List[tuple[re.Pattern, Callable[[re.Match], List[str]]]] = [
        (re.compile(r'next (\d+) days?'), lambda m: parse_next_n_days(int(m.group(1)))),
        (re.compile(r'([a-z]+ \d{1,2})-(\d{1,2}), (\d{4})'), parse_month_day_range),
    ]

    for pattern, handler in pattern_handlers:
        match = pattern.match(text)
        if match:
            return handler(match)

    # Try range parsing
    try:
        range_result = cal.evalRanges(text, base_date)
        if range_result:
            start_dt, end_dt = range_result[0]
            if start_dt and end_dt and start_dt != end_dt:
                return format_range(start_dt.date(), end_dt.date())
    except Exception:
        pass

    # Fallback: single date
    try:
        dt, _ = cal.parseDT(text, base_date)
        return [dt.strftime("%Y-%m-%d")]
    except Exception:
        return []
