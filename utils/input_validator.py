from typing import List, Optional, Tuple
import pandas as pd


class InputValidator:
    def __init__(self, df: pd.DataFrame):
        self.available_dates = set(df["date"])
        self.valid_room_types = set(df["room_type"].str.lower().unique())

    def validate(self, dates: List[str], room_type: Optional[str], room_count: Optional[int]) -> Tuple[bool, Optional[str]]:
        # Validate date format
        try:
            parsed_dates = pd.to_datetime(dates, format="%Y-%m-%d", errors="raise")
        except Exception:
            return False, "Invalid date format. Please use YYYY-MM-DD."

        # Validate dates exist in the data
        for d in parsed_dates:
            if d not in self.available_dates:
                return False, f"No data available for date: {d.date()}"

        # Validate room type
        if room_type is not None and room_type.lower() not in self.valid_room_types:
            return False, f"Invalid room type. Valid options are: {', '.join(self.valid_room_types)}"

        # Validate room count
        if room_count is not None and (not isinstance(room_count, int) or room_count <= 0):
            return False, "Room count must be an integer greater than zero."

        return True, None

