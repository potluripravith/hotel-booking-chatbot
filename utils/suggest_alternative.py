import pandas as pd
from typing import List, Optional, Tuple
from utils.load_data import DataLoader


class RoomAvailabilityService:
    def __init__(self, data_source: Optional[pd.DataFrame] = None):
        """
        Loads room data during initialization.
        """
        loader = DataLoader()
        self.df = data_source if data_source is not None else loader.load_room_data()

    def get_available_alternatives(
        self, date: str, exclude_room_type: Optional[str] = None
    ) -> List[Tuple[str, int, int]]:
        """
        Suggest available alternatives for a specific date (excluding a room type if needed).
        """
        df_date = self.df[self.df["date"] == date]
        if exclude_room_type:
            df_date = df_date[df_date["room_type"] != exclude_room_type]
        available = df_date[df_date["available_rooms"] > 0]

        return list(
            available[["room_type", "available_rooms", "price"]]
            .itertuples(index=False, name=None)
        )

    def suggest_cheaper_rooms(
        self, date: str, current_price: int
    ) -> List[Tuple[str, int]]:
        """
        Suggest cheaper room types available on a specific date.
        """
        df_date = self.df[
            (self.df["date"] == date) & (self.df["available_rooms"] > 0)
        ]
        cheaper = df_date[df_date["price"] < current_price]

        return list(
            cheaper[["room_type", "price"]].itertuples(index=False, name=None)
        )
