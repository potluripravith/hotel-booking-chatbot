import os
import pandas as pd
from typing import Dict, Optional

def load_room_data() -> pd.DataFrame:
    """
    Loads the room availability data from a CSV file.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'knowledge_base', 'Hotel_availability.csv')
    return pd.read_csv(csv_path)

def extract_room_prices(df: pd.DataFrame) -> Dict[str, int]:
    """
    Extracts fixed room prices from the availability dataframe.
    Assumes each room type has the same price across all dates.
    """
    room_price_map = df.drop_duplicates(subset=['room_type'])[['room_type', 'price']]
    return dict(zip(room_price_map['room_type'], room_price_map['price']))

def get_price_for_room(room_prices: Dict[str, int], room_type: str) -> Optional[int]:
    """
    Get fixed price for a given room type.
    """
    return room_prices.get(room_type)
def calculate_total_price(room_type: str, nights: int, count: int, price_map: dict) -> int:
    """Calculate total price for a single booking."""
    price = get_price_for_room(price_map, room_type)
    if price is None:
        return 0
    return price * nights * count

def calculate_combined_price(bookings: list[tuple[str, int, int]], price_map: dict) -> int:
    """
    Calculate total price for multiple bookings.
    Each booking is a tuple: (room_type, nights, room_count)
    """
    return sum(calculate_total_price(room_type, nights, count, price_map)
               for room_type, nights, count in bookings)