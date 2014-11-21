from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import authenticate, login


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'BookMarks.views.home'),
    url(r'^list/(?P<id>\d+)$', 'BookMarks.views.list'),
    url(r'^admin/(.*)', admin.site.urls),
    url(r'^new_list/', 'BookMarks.views.newList'),
    url(r'^new_link/(?P<listId>\d+)$', 'BookMarks.views.newLink'),
    url(r'^delete_lists/', 'BookMarks.views.deleteLists'),
    url(r'^delete_links/', 'BookMarks.views.deleteLinks'),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'), #django.contrib.auth.views.login
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/logged_out/'}),
    url(r'^logged_out/', 'BookMarks.views.logged_out'),
	url(r'^register/', 'BookMarks.views.register'),
 	url(r'^accounts/$', include('django.contrib.auth.urls')),
)
