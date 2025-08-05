
from typing import List, Dict,Tuple
from utils.price_utils import PriceCalculator

def price_calculation_node(
    room_type: str,
    room_count: int,
    dates: List[str],
    price_map: Dict[str, int]
) -> Tuple[str, int]:
    """
    Calculates total booking price for given room type, count, and dates.
    
    Parameters:
        room_type (str): The type of room user wants to book.
        room_count (int): Number of rooms user wants.
        dates (List[str]): List of booking dates in 'YYYY-MM-DD' format.
        price_map (Dict[str, int]): Precomputed room prices.

    Returns:
        Tuple[str, int]: Response message and total price.
    """
    price = PriceCalculator
    nights = len(dates)
    if nights == 0 or room_count <= 0 or not room_type:
        return "Booking details are incomplete. Please provide room type, room count, and valid dates.", 0

    total_price = price.calculate_total_price(room_type, nights, room_count, price_map)

    if total_price == 0:
        return f"Sorry, we couldn't calculate the price for the '{room_type}' room.", 0


    return total_price
