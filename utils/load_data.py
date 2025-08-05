import pandas as pd
import os
from typing import Optional

class DataLoader:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge_base')

    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Loads any CSV file from the knowledge_base directory.
        """
        path = os.path.join(self.base_path, filename)
        return pd.read_csv(path)

    def load_room_data(self) -> pd.DataFrame:
        return self.load_csv("Hotel_availability.csv")

    def load_faq_data(self) -> pd.DataFrame:
        return self.load_csv("Hotel_faqs.csv")
