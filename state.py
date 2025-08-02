from typing import TypedDict,Optional,Literal

class State(TypedDict):
    user_input: Optional[str]
    intent:Optional[Literal["booking", "faq", "price_enquiry", "alternative", "unknown"]]
    date:Optional[str]
    room_type:Optional[str]
    room_count: Optional[int]
    price: Optional[int]
    total_price: Optional[int]
