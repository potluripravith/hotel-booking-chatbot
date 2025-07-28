from datetime import datetime, timedelta
import parsedatetime as pdt
import pandas as pd
from typing import List, Dict, Union

def load_room_data(path: str = "knowledge_base/room_availability.csv") -> pd.DataFrame:
    """
    Loads the room availability data from a CSV file
    """
    return pd.read_csv(path)


def normalize_date(date_str: str,base_date: datetime = None) -> List[str]:
    """
    Parses natural language date expressions and converts them to 'YYYY-MM-DD' format.
    
    Examples:
        "today" -> "2025-07-28"
        "next friday" -> "2025-08-01"
        "tomorrow" -> "2025-07-29"
        "15th August" -> "2025-08-15"
    
    Args:
        date_str (str): The natural language date string.
    
    Returns:
        str: The normalized date in 'YYYY-MM-DD' format or None if parsing fails.
    """
    cal = pdt.Calendar()
    base = base_date or datetime.now()
    text =date_str.strip().lower()
    
    try:
        start_date, end_date = cal.evalRanges(text, base)[0]
        return [(start_date + timedelta(days=i)).date().isoformat()
                for i in range((end_date - start_date).days + 1)]
    except (IndexError, TypeError):
        pass

    try:
        date_obj, _ = cal.parseDT(text, base)
        return [date_obj.date().isoformat()]
    except (ValueError, TypeError):
        return []


def check_availability(
    df: pd.DataFrame,
    dates: Union[str, List[str]],
    room_type: str = None,
    count: int = 1
) -> Union[bool, Dict[str, Union[str, Dict]]]:
    """
    Checks room availability for single or multiple dates.

    Args:
        df (pd.DataFrame): Room availability DataFrame.
        dates (str or List[str]): A single date or list of dates in 'YYYY-MM-DD' format.
        room_type (str, optional): Specific room type to check.
        count (int, optional): Number of rooms required.

    Returns:
        dict or bool: Availability status per date and room type.
    """

    if isinstance(dates, str):
        dates = [dates]

    results = {}

    for date in dates:
        day_df = df[df['date'] == date]

        if day_df.empty:
            results[date] = "No data available"
            continue

        if room_type:
            rt_df = day_df[day_df['room_type'].str.lower() == room_type.lower()]
            if rt_df.empty:
                results[date] = f"{room_type} not available"
            else:
                available_rooms = rt_df.iloc[0]['available_rooms']
                if available_rooms >= count:
                    results[date] = f"{available_rooms} {room_type} room(s) available"
                else:
                    results[date] = f"Only {available_rooms} {room_type} room(s) available, need {count}"
        else:
            availability = {
                row['room_type']: f"{row['available_rooms']} room(s) available"
                for _, row in day_df.iterrows()
                if row['available_rooms'] > 0
            }
            if availability:
                results[date] = availability
            else:
                results[date] = "No rooms available"

    return results if len(dates) > 1 or room_type is None else list(results.values())[0]