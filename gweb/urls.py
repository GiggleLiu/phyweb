from django.conf.urls import patterns, include, url
from gweb import views
from django.contrib import admin
admin.autodiscover()

handler404 = 'lala.views.page_not_found'
handler500 = 'lala.views.page_error'
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lala.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^help/(.+)/$',views.gethelp,name='gethelp'),
    url(r'^$|^nav/$|^index/$|^index/default/$',views.mainpage,name='mainpage'),
    url(r'^login/$',views.login,name='login'),
    url(r'^latex/$',views.latex,name='latex'),
    url(r'^help/(.+)/$',views.gethelp,name='gethelp'),
    url(r'^comments/delete_own/(?P<id>.*)/$', views.delete_own_comment, name='delete_own_comment'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^being/', include('being.urls')),
    url(r'^notice/', include('notice.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^topic/', include('essay.urls')),
    #url(r'^comments/', include('django_comments.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    #url('', include('django_socketio.urls')),
    #url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': '/media'}),
)
