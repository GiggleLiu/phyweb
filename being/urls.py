from django.conf.urls import patterns, include, url
from being import views

urlpatterns = patterns('',
    # Examples:
    url(r'^logout/$', views.logout,name='logout'),
    url(r'^login/$', views.login,name='login'),
    url(r'^user_detail/(\d+)', views.user_detail,name='user_detail'),
    url(r'^call/(\d+)', views.user_call,name='call'),
    url(r'^user_update/', views.user_update,name='user_update'),
    url(r'^being_update/', views.being_update,name='being_update'),
    url(r'^register_step1/',views.register_step1,name='register_step1'),
    url(r'^register_step2/',views.register_step2,name='register_step2'),
    url(r'^register_success/',views.register_success,name='register_success'),
    url(r'^register_step2/(\d+)/',views.register_step2,name='redirectto_register_step2'),
    url(r'^update_password/$', views.update_password,name='update_password'),
)
