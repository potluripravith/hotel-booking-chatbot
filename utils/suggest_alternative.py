import pandas as pd
from typing import List, Optional, Tuple
import os
def load_room_data() -> pd.DataFrame:
    """
    Loads the room availability data from a CSV file.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'knowledge_base', 'Hotel_availability.csv')
    return pd.read_csv(csv_path)
def get_available_alternatives(
    df: pd.DataFrame, 
    date: str, 
    exclude_room_type: Optional[str] = None
) -> List[Tuple[str, int, int]]:
    """
    Suggest available alternatives for a specific date (excluding a room type if needed).
    """
    df_date = df[df["date"] == date]
    if exclude_room_type:
        df_date = df_date[df_date["room_type"] != exclude_room_type]
    available = df_date[df_date["available_rooms"] > 0]
    
    return list(available[["room_type", "available_rooms", "price"]].itertuples(index=False, name=None))

def suggest_cheaper_rooms(
    df: pd.DataFrame, 
    date: str, 
    current_price: int
) -> List[Tuple[str, int]]:
    """
    Suggest cheaper room types available on a specific date.
    """
    df_date = df[(df["date"] == date) & (df["available_rooms"] > 0)]
    cheaper = df_date[df_date["price"] < current_price]
    
    return list(cheaper[["room_type", "price"]].itertuples(index=False, name=None))
