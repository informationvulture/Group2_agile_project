"""
This is the Selenium implimenation of testing our web app.
"""

import unittest
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):

        # This is the path to the firefoxdriver executable
        # Since this is originally done on GitHub Codespaces,
        # we need to set it to run as headless.
        
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts)

    def test_signup_page(self):

        driver = self.driver
        driver.get("http://127.0.0.1:8080/signup")
        self.assertIn("Sign Up", driver.title)
        self.assertNotIn("No results found.", driver.page_source)

    def test_non_existant(self):

        driver = self.driver
        driver.get("http://127.0.0.1:8080/nonexistant")
        self.assertIn("Not Found", driver.page_source)

    def test_first_game(self):
        
        driver = self.driver
        driver.get("http://127.0.0.1:8080/view/1")
        self.assertIn("Trivia Game", driver.page_source)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()