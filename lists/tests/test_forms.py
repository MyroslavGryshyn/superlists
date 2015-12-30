from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR 
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
