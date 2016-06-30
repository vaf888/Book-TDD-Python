from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/the-only-list-in-the-world/$', 'lists.views.list_view', name='list_view'),
    # url(r'^admin/', include(admin.site.urls)),
]

