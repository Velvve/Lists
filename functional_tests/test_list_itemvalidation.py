from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """Тест валидации элемента списка"""

    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        # Эдит добавляет домашнюю страницу и случайно пытается
        # отправить пустой элемент списка. Она нажимает Enter
        self.fail('Напиши меня')
