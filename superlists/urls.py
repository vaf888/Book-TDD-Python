from django.conf.urls import patterns, include, url
from lists import views

urlpatterns = [
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/', include('lists.urls')), 
]

