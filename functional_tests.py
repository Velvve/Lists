from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest


class NewVisitorTest(unittest.TestCase):
    """тест нового посетитея"""

    def setUp(self) -> None:
        """установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """демонтаж"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно начать список и получить его позже """
        # домашняя страница
        self.browser.get('http://localhost:8000')
        # заголовок и шапка страниц
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element('tag name', 'h1').text
        self.assertIn('To-Do', header_text)

        # предлагается ввести элемент списка
        inputbox = self.browser.find_element('id', 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element('id', 'id_list_table')
        rows = table.find_elements('tag name', 'tr')
        self.assertIn('1: Купить павлиньи перья', [row.text for row in rows])

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент
        # Она вводит  "Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element('id', 'id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Таблица обновляется  и теперь показывает оба элемента ее списка
        table = self.browser.find_element('id', 'id_list_table')
        rows = table.find_elements('tag name', 'tr')
        self.assertIn('1: Купить павлиньи перья', [row.text for row in rows])
        self.assertIn(
            '2: Сделать мушку из павлиньих перьев',
            [row.text for row in rows]
        )

        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
