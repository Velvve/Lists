from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """тест нового посетитея"""

    def setUp(self) -> None:
        """установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Ожидание строки в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element('id', 'id_list_table')
                rows = table.find_elements('tag name', 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_it_user(self):
        """тест: можно начать список для одного пользователя """
        # домашняя страница
        self.browser.get(self.live_server_url)
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
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент
        # Она вводит  "Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element('id', 'id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Таблица обновляется  и теперь показывает оба элемента ее списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """тест: многочисленные пользователи могут начать списки по разным url"""
        # Эдит хочет начать новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element('id', 'id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Она замечает что ее список имеет уникальный URL- адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/list/.+')

        # Теперь новый пользователь, Френсис, переходит на сайт.

        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Френсис посещает домашнюю страницу. Нет некаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element('tag name', 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку ', page_text)

        # Френсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Эдит
        inputbox = self.browser.find_element('id', 'id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Френсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/list/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element('tag name', 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
