from typing import List, Optional, Tuple, Union
import pandas as pd
from utils.load_data import DataLoader
from utils.input_validator import InputValidator
from utils.availability_checker import AvailabilityChecker


class AvailabilityService:
    def __init__(self):
        loader = DataLoader()
        self.df = loader.load_room_data()
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.validator = InputValidator(self.df)
        self.checker = AvailabilityChecker()

    def check_availability(
        self,
        dates: List[str],
        room_type: Optional[str] = None,
        room_count: Optional[int] = None
    ) -> Tuple[bool, Union[str, dict, list, int]]:

        is_valid, error = self.validator.validate(dates, room_type, room_count)
        if not is_valid:
            return False, error

        parsed_dates = pd.to_datetime(dates)
        filtered_df = self.df[self.df["date"].isin(parsed_dates)]

        if len(parsed_dates) == 1:
            return self.checker.check_single_date(parsed_dates[0], filtered_df, room_type, room_count)
        else:
            return self.checker.check_range_dates(parsed_dates, filtered_df, room_type, room_count)
