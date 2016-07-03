from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item
from lists.views import home_page

class HomePageTest(TestCase):

    def test_home_page_is_about_todo_lists(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

class NewListViewTest(TestCase):

    ## MY - each test should test a single item
    ## rule of thumb - in general, one assertion
    ## Tests should do:
    ## i) save item to database
    ## ii) after that, redirect

    def test_home_page_can_save_post_requests_to_database(self):
        self.client.post('/lists/new',{'item_text': 'A new item'})
        item_from_db = Item.objects.all()[0]
        self.assertEqual(item_from_db.text, 'A new item')

    def test_redirects_to_list_url(self):
        response=self.client.post('/lists/new',{'item_text': 'A new item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_lists_shows_items_in_database(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        ## MY -replacing code below, using django test
        ## internal functions
        #request = HttpRequest()
        #response = home_page(request)
        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertIn('item 1', response.content.decode())
        ## MY - using assert from Django 
        self.assertContains(response,'item 2')



class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

