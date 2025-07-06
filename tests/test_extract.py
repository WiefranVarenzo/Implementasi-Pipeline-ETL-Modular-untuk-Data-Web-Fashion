import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils import extract
from requests.exceptions import RequestException

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.html = '''
            <div class="product-details">
                <h3 class="product-title">Unknown Product</h3>
                <div class="price-container"><span class="price">$100.00</span></div>
                <p>Rating: ⭐ Invalid Rating / 5</p>
                <p>5 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        '''
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.article = self.soup.find('div', class_='product-details')

    def test_extract_fashion_data(self):
        result = extract.parse_product_element(self.article)
        expected = {
            "Title": "Unknown Product",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ Invalid Rating / 5",
            "Colors": "5 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men"
        }
        self.assertEqual(result, expected)

    @patch("utils.extract.requests.get")
    def test_fetching_content_success(self, mock_get):
        html = "<html><body><h1>Test Page</h1></body></html>"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        content = extract.fetch_html("https://fashion-studio.dicoding.dev")
        self.assertIn("<h1>Test Page</h1>", content)

    @patch("utils.extract.requests.get")
    def test_fetching_content_failure(self, mock_get):
        mock_get.side_effect = RequestException("Simulated connection error")
        result = extract.fetch_html("https://fail.com")
        self.assertIsNone(result)

    def test_parse_product_element_exception(self):
        class BrokenDiv:
            def find(self, *args, **kwargs):
                raise Exception("Broken find method")

            def find_all(self, *args, **kwargs):
                raise Exception("Broken find_all method")

        result = extract.parse_product_element(BrokenDiv())
        self.assertIsInstance(result, dict)
        self.assertIn("Title", result)

    def test_extract_all_products_valid(self):
        result = extract.extract_all_products(self.html)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Unknown Product")

    def test_extract_all_products_empty(self):
        html = "<html><body><div>No products here</div></body></html>"
        result = extract.extract_all_products(html)
        self.assertEqual(result, [])

    @patch("utils.extract.fetch_html", return_value="<html></html>")
    def test_scrape_fashion_products_with_empty_html(self, mock_fetch_html):
        result = extract.scrape_fashion_products("https://example.com", delay=0)
        self.assertEqual(result, [])

    @patch("utils.extract.fetch_html")
    def test_scrape_fashion_products_success(self, mock_fetch_html):
        mock_fetch_html.return_value = self.html
        result = extract.scrape_fashion_products("https://example.com", delay=0)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)
        self.assertIn("Title", result[0])

if __name__ == "__main__":
    unittest.main()
