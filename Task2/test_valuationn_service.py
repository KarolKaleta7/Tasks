import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from Valuation_service import (load_data,
                               create_currency_dict,
                               convert_price_to_pln,
                               calculate_total_price,
                               sort_data,
                               process_matching)

class TestProcessing(unittest.TestCase):
    
    def setUp(self):
        self.data = pd.DataFrame({
            'price': [10, 20, 30],
            'currency': ['USD', 'EUR', 'PLN'],
            'quantity': [1, 2, 3],
            'matching_id': [1, 2, 3]
        })
        self.currencies = pd.DataFrame({
            'currency': ['USD', 'EUR', 'PLN'],
            'ratio': [4.00, 4.50, 1.00]
        })
        self.matchings = pd.DataFrame({
            'matching_id': [1, 2, 3],
            'top_priced_count': [1, 2, 1]
        })

    def test_read_data(self):
        data, currencies, matchings = load_data()

        self.assertEqual(data.shape[0], 9)
        self.assertEqual(data.shape[1], 5)

        self.assertEqual(currencies.shape[0], 3)
        self.assertEqual(currencies.shape[1], 2)

        self.assertEqual(matchings.shape[0], 3)
        self.assertEqual(matchings.shape[1], 2)


    def test_create_currency_dict(self):
        expected_dict = {'USD': 4.00, 'EUR': 4.50, 'PLN': 1.00}
        result_dict = create_currency_dict(self.currencies)
        self.assertEqual(result_dict, expected_dict)

    def test_convert_price_to_pln(self):
        expected_data = self.data.copy()
        expected_data['price_in_pln'] = [40.0, 90.0, 30.0]
        result_data = convert_price_to_pln(self.data, create_currency_dict(self.currencies))
        assert_frame_equal(result_data, expected_data)

    def test_calculate_total_price(self):
        data_with_price_in_pln = convert_price_to_pln(self.data, create_currency_dict(self.currencies))
        expected_data = data_with_price_in_pln.copy()
        expected_data['total_price'] = [40.0, 180.0, 90.0]
        result_data = calculate_total_price(data_with_price_in_pln)
        assert_frame_equal(result_data, expected_data)

    def test_process_matching(self):
        data_sorted = sort_data(calculate_total_price(convert_price_to_pln(self.data, create_currency_dict(self.currencies))))
        expected_output = pd.DataFrame({
            'matching_id': [1, 2, 3],
            'total_price': [40.0, 180.0, 90.0],
            'avg_price': [40.0, 90.0, 30.0],
            'currency': ['PLN', 'PLN', 'PLN'],
            'ignored_products_count': [0, 0, 0]
        })
        result_output = process_matching(data_sorted, self.matchings)
        assert_frame_equal(result_output, expected_output)

if __name__ == '__main__':
    unittest.main()