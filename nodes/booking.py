# from utils.check_availability import check_availability
# from state import State
# from llm import extract_booking_info

# def booking_node(state:State)->State:
#     user_input = state.get("user_input", "")
#     extracted = extract_booking_info(user_input)
    
#     date = extracted.get("date")
#     room_type = extracted.get("room_type")
#     room_count = extracted.get("room_count")
    
#     is_available, data = check_availability(date,room_type,room_count)
    
#     if is_available:
#         print(f"🤖: Great news! We have {room_count} {room_type or 'room'} available on {date}.")
#         print("🤖: Shall I proceed with the booking?")
        
#     else:
#         print(f"🤖: I'm sorry, we don't have availability for {room_type or 'that room'} on {date}.")
#         print(f"🤖: {data}" )
