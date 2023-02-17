from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
from selenium import webdriver


class ItemValidationTest(FunctionalTest):
    """Тест валидации элемента списка"""

    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        # Эдит добавляет домашнюю страницу и случайно пытается
        # отправить пустой элемент списка. Она нажимает Enter
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Домашняя страница обновляется, и появляется сообщение об ошибке
        self.wait_for(lambda:
                      self.browser.find_element('css selector', '#id_text:invalid'
                                                ))

        # Она пробует снова теперь с неким текстом для элемента и это работает
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda:
                      self.browser.find_element('css selector', '#id_text:valid'
                                                ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda:
                      self.browser.find_element('css selector', '#id_text:invalid'
                                                ))

        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda:
                      self.browser.find_element('css selector', '#id_text:valid'
                                                ))

        # Заполнение новыми элементами
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        """тест: нельзя добавлять повторяющиеся элементы"""
        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # Она пытается ввести повторяющийся элемент
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Она видит полезное сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element('css selector', '.has-error').text,
            "You've already got this in your list"
        ))


