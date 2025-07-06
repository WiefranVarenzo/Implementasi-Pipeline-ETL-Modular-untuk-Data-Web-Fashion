import unittest
import pandas as pd
from utils import transform
from datetime import datetime

class TestTransformData(unittest.TestCase):

    def setUp(self):
        self.exchange_rate = 16000
        self.valid_data = pd.DataFrame({
            'Title': ['T-Shirt', 'Dress'],
            'Price': ['$100.00', '$200.00'],
            'Rating': ['4.5 out of 5', '4.0 out of 5'],
            'Colors': ['Colors 2', 'Colors 3'],
            'Size': ['Size: M', 'Size: L'],
            'Gender': ['Gender: Men', 'Gender: Women']
        })

    def test_transform_valid_data(self):
        result = transform.transform_data(self.valid_data.copy(), self.exchange_rate)
        self.assertEqual(len(result), 2)
        self.assertIn('Extraction Timestamp', result.columns)
        self.assertAlmostEqual(result.iloc[0]['Price'], 1600000.0, places=2)
        self.assertEqual(result.iloc[1]['Rating'], 4.0)
        self.assertEqual(result.iloc[1]['Colors'], 3)
        self.assertEqual(result.iloc[1]['Size'], 'L')


    def test_filter_invalid_title(self):
        data = self.valid_data.copy()
        data.loc[0, 'Title'] = 'Unknown Product'
        result = transform.transform_data(data, self.exchange_rate)
        self.assertEqual(len(result), 1)

    def test_filter_invalid_rating(self):
        data = self.valid_data.copy()
        data.loc[0, 'Rating'] = 'Invalid Rating'
        result = transform.transform_data(data, self.exchange_rate)
        self.assertEqual(len(result), 1)

    def test_filter_invalid_price(self):
        data = self.valid_data.copy()
        data.loc[0, 'Price'] = 'Price Unavailable'
        result = transform.transform_data(data, self.exchange_rate)
        self.assertEqual(len(result), 1)

    def test_drop_duplicates_by_title(self):
        data = pd.concat([self.valid_data, self.valid_data])
        result = transform.transform_data(data, self.exchange_rate)
        self.assertEqual(len(result), 2)

    def test_dropna_on_essential_columns(self):
        data = self.valid_data.copy()
        data.loc[0, 'Price'] = None
        result = transform.transform_data(data, self.exchange_rate)
        self.assertEqual(len(result), 1)

    def test_key_error_handling(self):
        data = self.valid_data.drop(columns=['Rating'])
        result = transform.transform_data(data, self.exchange_rate)
        self.assertTrue(result.empty)

    def test_value_error_handling(self):
        data = self.valid_data.copy()
        data['Price'] = ['ABC', '$20.00']
        result = transform.transform_data(data, self.exchange_rate)
        self.assertTrue(result.empty)

    def test_generic_exception_handling(self):
        data = self.valid_data.copy()
        data['Colors'] = ['two', 'three']  
        result = transform.transform_data(data, self.exchange_rate)
        self.assertTrue(result.empty)

    def test_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = transform.transform_data(empty_df, self.exchange_rate)
        self.assertTrue(result.empty)

    def test_invalid_rating_format(self):
        data = self.valid_data.copy()
        data['Rating'] = ['Rating is bad', 'Still bad']
        result = transform.transform_data(data, self.exchange_rate)
        self.assertTrue(result.empty)

    def test_empty_string_price(self):
        data = self.valid_data.copy()
        data['Price'] = ['', '$20.00']
        result = transform.transform_data(data, self.exchange_rate)
        self.assertTrue(result.empty)

    def test_transform_to_dataframe_with_invalid_input(self):
        result = transform.transform_to_DataFrame("just string")
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()
