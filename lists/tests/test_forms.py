from django.test import TestCase

from lists.forms import (
    ExistingListItemForm, ItemForm, 
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
)

from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_renders_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())

    def test_form_validates_blank_line(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_can_save_item(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': "Do me"})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())


class ExistingListItemFormTest(TestCase):

    def test_form_renders_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validates_blank_line(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_validates_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [DUPLICATE_ITEM_ERROR]
        )

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': "hi"})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())

