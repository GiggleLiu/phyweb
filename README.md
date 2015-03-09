#run this app
###make ckeditor work
mkdir static/media
mkdir static/media/ckeditor
change site-packages/ckeditor/urls.py line 1 from
        from django.conf.urls.defaults import patterns,url
to
        from django.conf.urls import patterns,url
