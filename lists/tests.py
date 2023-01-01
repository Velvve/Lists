import time

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List


class HomePageTest(TestCase):
    """тест домашней страницы"""

    def test_used_home_template(self):
        """тест: используется домашний шаблон"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndModelsTest(TestCase):
    """Тест модели элемента списка"""

    def test_saving_and_retrieving_items(self):
        """Тест на сохранение и получения элементов списка"""
        list_ = List()
        list_.save()
        fitst_item = Item()
        fitst_item.text = 'The first (ever) list item'
        fitst_item.list = list_
        fitst_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


def test_display_all_items():
    """тест: отображаются все элементы списка"""
    list_ = List.objects.create()
    Item.objects.create(text='itemey 1', list=list_)
    Item.objects.create(text='itemey 2', list=list_)


class ListViewTest(TestCase):
    """тест представления списка"""

    def test_uses_list_template(self):
        """тест: используется шаблон списка"""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        """тест: отображаются все элементы списка"""
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Другой элемент 1 списка', list=other_list)
        Item.objects.create(text='Другой элемент 2 списка', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'Другой элемент 1 списка')
        self.assertNotContains(response, 'Другой элемент 2 списка')

    def test_passes_correct_list_to_template(self):
        """тест: передается правильный шаблон списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)



class NewListTest(TestCase):
    """тест нового списка"""

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после post-запроса"""
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        list_new = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_new.id}/')


class NewItemTest(TestCase):
    """Тест нового элемента списка"""

    def test_can_save_a_post_request_to_an_existing_list(self):
        """Тест: можно сохранить post-запрос в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        """тест: переадресуется в представление списка"""
        other_list = List.objects.create()
        corrent_list = List.objects.create()

        response = self.client.post(f'/lists/{corrent_list.id}/add_item',
                                    data={'item_text': 'A new item for an existing list'})

        self.assertRedirects(response, f'/lists/{corrent_list.id}/')
