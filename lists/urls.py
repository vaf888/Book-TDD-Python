from django.conf.urls import patterns,url
from lists import views

urlpatterns = [
    url(r'^new$', 'lists.views.new_list', name='new_list'),
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^(\d+)/add$', 'lists.views.add_item', name='add_item'),
]

