from django.conf.urls import patterns, include, url
from fshare import views
from django.contrib import admin
admin.autodiscover()

handler404 = 'lala.views.page_not_found'
handler500 = 'lala.views.page_error'
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', views.server, name='inner'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^new/', views.file_new,name='file_new'),
    url(r'^delete/(\d+)', views.file_delete,name='file_delete'),

    #url('', include('django_socketio.urls')),
    #url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': '/media'}),
)
