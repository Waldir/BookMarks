from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'BookMarks.views.home'),
    url(r'^list/(?P<id>\d+)$', 'BookMarks.views.list'),
    url(r'^admin/(.*)', admin.site.urls),
    url(r'^accounts/', include('registration.urls')),
    url(r'^new_list/', 'BookMarks.views.newList'),
    url(r'^new_link/(?P<listId>\d+)$', 'BookMarks.views.newLink'),
    url(r'^delete_lists/', 'BookMarks.views.deleteLists'),
    url(r'^delete_links/', 'BookMarks.views.deleteLinks'),
	url(r'^accounts/login/$', 'BookMarks.views.login'), #django.contrib.auth.views.login
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
	url(r'^register/', 'BookMarks.views.register'),
 	url(r'^accounts/$', include('django.contrib.auth.urls')),

)
