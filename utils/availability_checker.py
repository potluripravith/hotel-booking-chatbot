from typing import List, Optional, Tuple
import pandas as pd


class AvailabilityChecker:
    def check_single_date(
        self,
        date: pd.Timestamp,
        filtered_df: pd.DataFrame,
        room_type: Optional[str],
        room_count: Optional[int]
    ) -> Tuple[bool, str | dict | list | int]:

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

    def check_range_dates(
        self,
        dates: List[pd.Timestamp],
        filtered_df: pd.DataFrame,
        room_type: Optional[str],
        room_count: Optional[int]
    ) -> Tuple[bool, str | dict | list | int]:

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
