from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


class HomeTestCase(TestCase):

    def test_root_url_resolves_to_home_page_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertTrue(response.content.decode(), expected_html)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')
        
    def test_displays_only_items_for_the_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='1 Item', list=correct_list)
        Item.objects.create(text='2 Item', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other 1 Item', list=other_list)
        Item.objects.create(text='other 2 Item', list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, "1 Item")
        self.assertContains(response, "2 Item")
        self.assertNotContains(response, "other 1 Item")
        self.assertNotContains(response, "other 2 Item")


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)

    def test_list_page_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': "A new list item"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirecting_after_POST_request(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': "A new list item"}
        )
        
        new_list = List.objects.first()
        self.assertRedirects(
            response, '/lists/{}/'.format(new_list.id))

class NewItemTest(TestCase):

    def test_can_save_item_after_POST_request(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            "/lists/{}/add_item".format(correct_list.id),
            data={'item_text': "A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = List.objects.first()
        self.assertEqual(
            new_item_text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            "/lists/{}/add_item".format(correct_list.id),
            data={'item_text': "A new item for an existing list"}
        )

        self.assertRedirects(
            response, "/lists/{}/".format(correct_list.id))

