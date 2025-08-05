import unittest
from nodes.check_availability import check_availability_node
from nodes.ask_roomtype import ask_room_type_node
from nodes.ask_roomcount import ask_room_count_node
from nodes.ask_room_type_and_count import ask_room_type_and_count_node
from unittest.mock import patch

class TestCheckAvailabilityNode(unittest.TestCase):

    @patch("utils.check_availability.AvailabilityService")
    def test_all_fields_provided_and_available(self, MockService):
        mock_instance = MockService.return_value
        mock_instance.check_availability.return_value = (True, [])

        state = {
            "date": "2025-08-05",
            "room_type": "King",
            "room_count": 2
        }

        next_node, state = check_availability_node(state)
        self.assertEqual(next_node, "proceed_to_price")
        print(f"\n[proceed_to_price] agent_message: {state.get('agent_message')}")

    @patch("utils.check_availability.AvailabilityService")
    def test_missing_room_type(self, MockService):
        mock_instance = MockService.return_value
        mock_instance.check_availability.return_value = (True, [
            {"room_type": "Single", "available_rooms": 2},
            {"room_type": "King", "available_rooms": 1}
        ])

        state = {
            "date": "2025-08-05",
            "room_count": 2
        }

        next_node, state = check_availability_node(state)
        self.assertEqual(next_node, "ask_room_type")

        state = ask_room_type_node(state)
        print(f"\n[ask_room_type] agent_message: {state.get('agent_message')}")

    @patch("utils.check_availability.AvailabilityService")
    def test_missing_room_count(self, MockService):
        mock_instance = MockService.return_value
        mock_instance.check_availability.return_value = (True, [
            {"room_type": "King", "available_rooms": 2}
        ])

        state = {
            "date": "2025-08-05",
            "room_type": "King"
        }

        next_node, state = check_availability_node(state)
        self.assertEqual(next_node, "ask_room_count")

        state = ask_room_count_node(state)
        print(f"\n[ask_room_count] agent_message: {state.get('agent_message')}")

    @patch("utils.check_availability.AvailabilityService")
    def test_missing_both_room_type_and_count(self, MockService):
        mock_instance = MockService.return_value
        mock_instance.check_availability.return_value = (True, [
            {"room_type": "Single", "available_rooms": 2},
            {"room_type": "King", "available_rooms": 3},
            {"room_type": "Suite", "available_rooms": 1},
            {"room_type": "Luxury", "available_rooms": 1},
        ])

        state = {
            "date": "2025-08-05"
        }

        next_node, state = check_availability_node(state)
        self.assertEqual(next_node, "ask_both")

        state = ask_room_type_and_count_node(state)
        print(f"\n[ask_room_type_and_count] agent_message: {state.get('agent_message')}")

    @patch("utils.check_availability.AvailabilityService")
    def test_no_availability(self, MockService):
        mock_instance = MockService.return_value
        mock_instance.check_availability.return_value = (False, "King not available with 5 rooms on 2025-08-05")

        state = {
            "date": "2025-08-05",
            "room_type": "King",
            "room_count": 5
        }

        next_node, state = check_availability_node(state)
        self.assertEqual(next_node, "wait_input")
        print(f"\n[no_availability] agent_message: {state.get('agent_message')}")


if __name__ == "__main__":
    unittest.main()
