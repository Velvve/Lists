import os
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """Функциональный тест"""

    def setUp(self) -> None:
        """установка"""
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self) -> None:
        """демонтаж"""
        self.browser.quit()

    @wait
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

    @wait
    def wait_for(self, fn):
        """ожидание"""
        return fn()

    def get_item_input_box(self):
        """получить поле ввода для элемента"""
        return self.browser.find_element('id', 'id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        """ожидание входа в систему"""
        self.wait_for(
            lambda: self.browser.find_element('link text', 'Log out')
        )
        navbar = self.browser.find_element('css selector', '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """ожидать выхода из системы"""
        self.wait_for(
            lambda: self.browser.find_element('name', 'email')
        )
        navbar = self.browser.find_element('css selector', '.navbar')
        self.assertNotIn(email, navbar.text)
