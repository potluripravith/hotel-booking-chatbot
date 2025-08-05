from typing import Dict, Optional
from utils.load_data import DataLoader
import pandas as pd

class PriceCalculator:
    def __init__(self):
        loader = DataLoader()
        self.df: pd.DataFrame = loader.load_room_data() 
        self.room_prices: Dict[str, int] = self._extract_room_prices()

    def _extract_room_prices(self) -> Dict[str, int]:
        """
        Extracts fixed room prices using self.df loaded in __init__.
        Assumes each room type has the same price across all dates.
        """
        room_price_map = self.df.drop_duplicates(subset=['room_type'])[['room_type', 'price']]
        return dict(zip(room_price_map['room_type'], room_price_map['price']))

    def get_price_for_room(self, room_type: str) -> Optional[int]:
        """Returns the fixed price for a given room type."""
        return self.room_prices.get(room_type)

    def calculate_total_price(self, room_type: str, nights: int, count: int) -> int:
        """Calculate total price for a single room booking."""
        price = self.get_price_for_room(room_type)
        if price is None:
            return 0
        return price * nights * count

    def calculate_combined_price(self, bookings: list[tuple[str, int, int]]) -> int:
        """
        Calculate total price for multiple bookings.
        Each booking is a tuple: (room_type, nights, room_count)
        """
        return sum(self.calculate_total_price(room_type, nights, count)
                   for room_type, nights, count in bookings)
