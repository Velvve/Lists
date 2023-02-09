from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


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

    def test_display_all_items(self):
        """тест: отображаются все элементы списка"""
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

    def test_cannot_save_empty_list_items(self):
        """тест: нельзя добавить пустой элемент списка"""
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()


