from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item
from lists.models import List 

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
        # expect that item saved as first element in db + redirected using
        # its id
        new_list = List.objects.first()
        self.assertRedirects(response,'/lists/%d/' % (new_list.id,))


class ListViewTest(TestCase):

    def test_lists_page_shows_items_in_database(self):

        our_list = List.objects.create()
        Item.objects.create(text='item 1', list=our_list)
        Item.objects.create(text='item 2', list=our_list)

        other_list = List.objects.create()
        Item.objects.create(text='not this one', list=other_list)
        

        ## MY -replacing code below, using django test
        ## internal functions
        #request = HttpRequest()
        #response = home_page(request)
        response = self.client.get('/lists/%d/' % (our_list.id,))

        self.assertContains(response,'item 1')
        self.assertContains(response,'item 2')
        self.assertNotContains(response,'not this one')
        

    def test_uses_lists_template(self):
        our_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (our_list.id,))
        self.assertTemplateUsed(response,'list.html')

    def test_passes_list_to_template(self):
        our_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (our_list.id,))
        self.assertEqual(response.context['list'], our_list)

class AddItemToExistingListTest(TestCase):

    def test_add_an_item_to_an_existing_list(self):
        our_list = List.objects.create()
        our_list = List.objects.create()
        self.client.post(
            '/lists/%d/add' % (our_list.id,),
            {'item_text': 'new item for my list'}
        )
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, our_list)
        self.assertEqual(new_item.text, 'new item for my list')

    def test_redirects_to_list_page(self):
        List.objects.create()
        our_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add' % (our_list.id,),
            {'item_text': 'new item fro my list'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/lists/%d/' % (our_list.id,))


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_list = List()
        first_list.save()

        first_item = Item()
        first_item.text = 'Item the first'
        first_item.list = first_list
        first_item.save()

        ''' second item goes to the same list '''
        second_item = Item()
        second_item.text = 'second item'
        second_item.list = first_list
        second_item.save()

        first_item_from_db=Item.objects.all()[0]
        self.assertEqual(first_item_from_db.text, 'Item the first')
        self.assertEqual(first_item_from_db.list, first_list)

        second_item_from_db=Item.objects.all()[1]
        self.assertEqual(second_item_from_db.text, 'second item')
        self.assertEqual(second_item_from_db.list, first_list)


