import unittest
from unittest.mock import patch
import pandas as pd
from utils.check_availability import AvailabilityService

class TestAvailabilityService(unittest.TestCase):

    def setUp(self):
        # Common DataFrame used in all tests
        self.test_df = pd.DataFrame({
            "date": ["2025-08-05", "2025-08-06", "2025-08-07"],
            "room_type": ["Deluxe", "Deluxe", "Suite"],
            "available_rooms": [5, 2, 1],
            "price": [100, 100, 200]
        })

    @patch("utils.check_availability.DataLoader")
    @patch("utils.check_availability.InputValidator")
    @patch("utils.check_availability.AvailabilityChecker")
    def test_invalid_input(self, mock_checker, mock_validator, mock_loader):
        mock_loader.return_value.load_room_data.return_value = self.test_df
        mock_validator.return_value.validate.return_value = (False, "Invalid input")

        service = AvailabilityService()
        result = service.check_availability(["invalid-date"], "Deluxe", 2)
        self.assertEqual(result, (False, "Invalid input"))

    @patch("utils.check_availability.DataLoader")
    @patch("utils.check_availability.InputValidator")
    @patch("utils.check_availability.AvailabilityChecker")
    def test_single_date_valid(self, mock_checker, mock_validator, mock_loader):
        mock_loader.return_value.load_room_data.return_value = self.test_df
        mock_validator.return_value.validate.return_value = (True, "")
        mock_checker.return_value.check_single_date.return_value = (True, "Room is available")

        service = AvailabilityService()
        result = service.check_availability(["2025-08-05"], "Deluxe", 2)
        self.assertEqual(result, (True, "Room is available"))

    @patch("utils.check_availability.DataLoader")
    @patch("utils.check_availability.InputValidator")
    @patch("utils.check_availability.AvailabilityChecker")
    def test_single_date_no_availability(self, mock_checker, mock_validator, mock_loader):
        mock_loader.return_value.load_room_data.return_value = self.test_df
        mock_validator.return_value.validate.return_value = (True, "")
        mock_checker.return_value.check_single_date.return_value = (False, "No availability")

        service = AvailabilityService()
        result = service.check_availability(["2025-08-07"], "Suite", 2)
        self.assertEqual(result, (False, "No availability"))

    @patch("utils.check_availability.DataLoader")
    @patch("utils.check_availability.InputValidator")
    @patch("utils.check_availability.AvailabilityChecker")
    def test_multiple_dates_all_available(self, mock_checker, mock_validator, mock_loader):
        mock_loader.return_value.load_room_data.return_value = self.test_df
        mock_validator.return_value.validate.return_value = (True, "")
        mock_checker.return_value.check_multiple_dates.return_value = (True, "All dates available")

        service = AvailabilityService()
        result = service.check_availability(["2025-08-05", "2025-08-06"], "Deluxe", 2)
        self.assertEqual(result, (True, "All dates available"))

    @patch("utils.check_availability.DataLoader")
    @patch("utils.check_availability.InputValidator")
    @patch("utils.check_availability.AvailabilityChecker")
    def test_multiple_dates_all_available(self, mock_checker, mock_validator, mock_loader):
        mock_loader.return_value.load_room_data.return_value = self.test_df
        mock_validator.return_value.validate.return_value = (True, "")
        mock_checker.return_value.check_range_dates.return_value = (True, "All dates available")

        service = AvailabilityService()
        result = service.check_availability(["2025-08-05", "2025-08-06"], "Deluxe", 2)
        self.assertEqual(result, (True, "All dates available"))


    @patch("utils.check_availability.DataLoader")
    @patch("utils.check_availability.InputValidator")
    @patch("utils.check_availability.AvailabilityChecker")
    def test_multiple_dates_partial_availability(self, mock_checker, mock_validator, mock_loader):
        mock_loader.return_value.load_room_data.return_value = self.test_df
        mock_validator.return_value.validate.return_value = (True, "")
        mock_checker.return_value.check_range_dates.return_value = (False, "Some dates unavailable")

        service = AvailabilityService()
        result = service.check_availability(["2025-08-05", "2025-08-06"], "Deluxe", 4)
        self.assertEqual(result, (False, "Some dates unavailable"))
    @patch("utils.check_availability.DataLoader")
    @patch("utils.check_availability.InputValidator")
    @patch("utils.check_availability.AvailabilityChecker")
    def test_empty_date_list(self, mock_checker, mock_validator, mock_loader):
        mock_loader.return_value.load_room_data.return_value = self.test_df
        mock_validator.return_value.validate.return_value = (False, "Date list is empty")

        service = AvailabilityService()
        result = service.check_availability([])
        self.assertEqual(result, (False, "Date list is empty"))

if __name__ == "__main__":
    unittest.main()
