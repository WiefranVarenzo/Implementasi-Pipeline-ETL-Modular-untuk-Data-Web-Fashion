import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils import load
import warnings

class TestLoad(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Title": ["Sweater"],
            "Price": [50000.0],
            "Rating": [4.9],
            "Colors": [2],
            "Size": ["M"],
            "Gender": ["Unisex"],
            "Extraction Timestamp": ["2025-05-13"]
        })

    @patch("pandas.DataFrame.to_csv")
    def test_store_to_csv(self, mock_to_csv):
        load.store_to_csv(self.df)
        mock_to_csv.assert_called_once()

    @patch("utils.load.create_engine")
    def test_store_to_postgre(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        load.store_to_postgre(self.df, "postgresql://dummy")
        self.assertTrue(mock_engine.begin.called)

        mock_create_engine.side_effect = Exception("Connection failed")
        with self.assertRaises(Exception):
            load.store_to_postgre(self.df, "postgresql://dummy")
    
    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_store_to_sheets(self, mock_creds, mock_build):
        service = MagicMock()
        mock_build.return_value = service
        sheet = MagicMock()
        service.spreadsheets.return_value = sheet
        
        load.store_to_sheets(self.df)
        self.assertTrue(sheet.values.return_value.update.return_value.execute.called)

        mock_creds.side_effect = Exception("Credential issue")
        with self.assertRaises(Exception):
            load.store_to_sheets(self.df)

if __name__ == '__main__':
    unittest.main()
