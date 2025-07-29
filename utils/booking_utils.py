from datetime import datetime, timedelta
import parsedatetime as pdt
import os
from typing import List, Optional, Tuple,Callable
import pandas as pd


import re
def load_room_data() -> pd.DataFrame:
    """
    Loads the room availability data from a CSV file
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, '..', 'knowledge_base', 'Hotel_availability.csv')
    return pd.read_csv(path)

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


df = load_room_data()
df["date"] = pd.to_datetime(df["date"])

def validate_inputs(dates: List[str], room_type: Optional[str], room_count: Optional[int]) -> Tuple[bool, Optional[str]]:
    try:
        dates = pd.to_datetime(dates)
    except Exception:
        return False, "Invalid date format. Please use YYYY-MM-DD."

    # Validate date existence
    existing_dates = set(df["date"])
    for d in dates:
        if d not in existing_dates:
            return False, f"No data available for date: {d.date()}"

    # Validate room type
    valid_room_types = {"single", "king", "suite", "luxury"}
    if room_type is not None and room_type.lower() not in valid_room_types:
        return False, "We have only single, king, suite, and luxury room types."

    # Validate room count
    if room_count is not None and (not isinstance(room_count, int) or room_count <= 0):
        return False, "Room count must be an integer greater than zero."

    return True, None


def check_single_date(date, filtered_df, room_type, room_count):
    if room_type is None and room_count is None:
        available = filtered_df[filtered_df["available_rooms"] > 0]
        if available.empty:
            return False, f"No rooms available on {date.date()}"
        return True, available[["room_type", "available_rooms"]].to_dict("records")

    if room_type and room_count is None:
        rooms = filtered_df[filtered_df["room_type"].str.lower() == room_type.lower()]
        if rooms.empty or rooms.iloc[0]["available_rooms"] <= 0:
            return False, f"{room_type} not available on {date.date()}"
        return True, int(rooms.iloc[0]["available_rooms"])

    if room_type is None and room_count:
        valid = filtered_df[filtered_df["available_rooms"] >= room_count]
        if valid.empty:
            return False, f"No room type with at least {room_count} rooms on {date.date()}"
        return True, valid["room_type"].tolist()

    if room_type and room_count:
        row = filtered_df[
            (filtered_df["room_type"].str.lower() == room_type.lower()) &
            (filtered_df["available_rooms"] >= room_count)
        ]
        if not row.empty:
            return True, "Available"
        else:
            return False, f"{room_type} not available with {room_count} rooms on {date.date()}"


def check_range_dates(dates, filtered_df, room_type, room_count):
    if room_type is None and room_count is None:
        grouped = (
            filtered_df[filtered_df["available_rooms"] > 0]
            .groupby("room_type")["available_rooms"]
            .agg(["count", "min"])
        )
        valid = grouped[grouped["count"] == len(dates)]
        if valid.empty:
            return False, "No common room type available for all selected dates"
        return True, valid["min"].to_dict()

    if room_type and room_count is None:
        filtered = filtered_df[
            (filtered_df["room_type"].str.lower() == room_type.lower()) &
            (filtered_df["available_rooms"] > 0)
        ]
        if filtered["date"].nunique() != len(dates):
            missing = set(dates) - set(filtered["date"])
            return False, f"{room_type} not available on {', '.join(str(d.date()) for d in missing)}"
        return True, int(filtered["available_rooms"].min())

    if room_type is None and room_count:
        valid_by_date = filtered_df[filtered_df["available_rooms"] >= room_count]
        group = valid_by_date.groupby("date")
        if len(group) != len(dates):
            missing = set(dates) - set(group.groups.keys())
            return False, f"No room type with at least {room_count} rooms on {', '.join(str(d.date()) for d in missing)}"
        common = (
            valid_by_date.groupby("room_type")["available_rooms"]
            .agg(["count", "min"])
        )
        valid = common[common["count"] == len(dates)]
        if valid.empty:
            return False, "No common room types found for all dates"
        return True, valid["min"].to_dict()

    if room_type and room_count:
        match = filtered_df[
            (filtered_df["room_type"].str.lower() == room_type.lower()) &
            (filtered_df["available_rooms"] >= room_count)
        ]
        if match["date"].nunique() == len(dates):
            return True, "Available"
        else:
            missing = set(dates) - set(match["date"])
            return False, f"{room_type} not available with {room_count} rooms on {', '.join(str(d.date()) for d in missing)}"


def check_availability(
    dates: List[str],
    room_type: Optional[str] = None,
    room_count: Optional[int] = None
) -> Tuple[bool, str | dict | list | int]:
    
    # Step 1: Validate inputs
    is_valid, error = validate_inputs(dates, room_type, room_count)
    if not is_valid:
        return False, error

    dates = pd.to_datetime(dates)
    filtered_df = df[df["date"].isin(dates)]

    # Step 2: Delegate based on single/multiple date
    if len(dates) == 1:
        return check_single_date(dates[0], filtered_df, room_type, room_count)
    else:
        return check_range_dates(dates, filtered_df, room_type, room_count)
