from typing import TypedDict,Optional,Literal

class State(TypedDict):
    user_input: Optional[str]
    intent:Optional[Literal["booking", "faq", "price_enquiry", "alternative", "unknown"]]
    has_greeted: Optional[bool]
    date:Optional[str]
    room_type:Optional[str]
    room_count: Optional[int]
    agent_message: Optional[str] 
    price: Optional[int]
    total_price: Optional[int]
    
    fallback_message: Optional[str]

    thank_you_message:Optional[str]
