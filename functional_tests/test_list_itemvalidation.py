from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """Тест валидации элемента списка"""

    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        # Эдит добавляет домашнюю страницу и случайно пытается
        # отправить пустой элемент списка. Она нажимает Enter
        self.browser.get(self.live_server_url)
        self.browser.get_item_input_box().send_keys(Keys.ENTER)

        # Домашняя страница обновляется, и появляется сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element('css selector', '.has-error').text,
            "You can't have an empty list item"
        ))

        # Она пробует снова теперь с неким текстом для элемента и это работает
        self.browser.get_item_input_box().send_keys('Buy milk')
        self.browser.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Попытка отправить второй пустой список
        self.browser.get_item_input_box().send_keys(Keys.ENTER)

        # Эдит получает аналогичное предупреждение
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element('css selector', '.has-error').text,
            "You can't have an empty list item"
        ))

        # Заполнение новыми элементами
        self.browser.get_item_input_box().send_keys('Make tea')
        self.browser.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
