from typing import TypedDict,Optional,Literal,List

class State(TypedDict):
    user_input: Optional[str]
    intent:Optional[Literal["booking", "faq", "price_enquiry", "alternative", "fallback"]]
    has_greeted: Optional[bool]
    date:Optional[str]
    room_type:Optional[str]
    room_count: Optional[int]
    agent_message: Optional[str] 
    price: Optional[int]
    total_price: Optional[int]
    availability_data:Optional[dict]
    fallback_message: Optional[str]
    memory: Optional[List[str]]

    thank_you_message:Optional[str]
