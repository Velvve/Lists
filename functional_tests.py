from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    """тест нового посетитея"""

    def setUp(self) -> None:
        """установка"""
        self.bowser = webdriver.Firefox()

    def tearDown(self) -> None:
        """демонтаж"""
        self.bowser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно начать список и получить его позже """
        # домашняя страница
        self.bowser.get('http://localhost:8000')
        # заголовок и шапка страниц
        self.assertIn('To-Do', self.bowser.title)
        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')