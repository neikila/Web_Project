from django.conf.urls import patterns, include, url
from django.contrib import admin
#from views import hello
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neikila.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^test2$','neikila.views.test2'),
    url(r'^accounts/login/$','django.contrib.auth.views.login'),
    url(r'^accounts/logout/$','django.contrib.auth.views.logout', {'next_page':'/accounts/login/'}),
    url(r'^accounts/profile/$','neikila.views.profile'),
    url(r'^settings$','neikila.views.settings'),
    url(r'^search$','neikila.views.search'),
    url(r'^settings/save$','neikila.views.save'),
    url(r'^ask$','neikila.views.ask_question'),
    url(r'^signin$','neikila.views.signin'),
    url(r'^like/$','neikila.views.like'),
    url(r'^hott/$','neikila.views.index', { 'sort': 'hot' } ),
    url(r'^answer$','neikila.views.answers'),
#    url(r'^question/(?P<id>\d+$','neikila.views.index', {}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','neikila.views.index'),
)
