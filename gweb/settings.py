"""
Django settings for gweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y38wm6%=kx9sf)$q^p6y_6ldi2nbed8a)3*pj-!c=vx3#5mgn5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS=(
        os.path.join(BASE_DIR, 'template').replace('\\','/'),
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.sites',
    #'notification',
    #'django_comments',
    'bootstrapform',
    'notice',
    'being',
    'south',
    'essay',
    'fshare',
    'ckeditor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gweb.urls'

WSGI_APPLICATION = 'gweb.wsgi.application'
#MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_ROOT=os.path.join(os.path.dirname(__file__), '../static/media').replace('\\','/')
MEDIA_URL="/static/media/"


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
ADMINS=(
        ('cacate','cacate0129@gmail.com'),
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': 'country',
        'NAME': './data.db',
        'USER':'postgres',
        'PASSWORD':'liujinguo',
        #'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT =os.path.join(os.path.dirname(__file__),'..')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'
SITE_ID = 1
EMAIL_HOST_USER = 'postmaster@yanglala.com'
EMAIL_HOST_PASSWORD = 'cacate0129'
EMAIL_HOST = 'smtp.yanglala.com'
#SESSION_COOKIE_DOMAIN=".dominio.com"
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT,'ckeditor')
CKEDITOR_IMAGE_BACKEND='pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':'Uni',
        'height':'500',
        'width':'100%',
    },
}
TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"gweb.context_processor.myprocessor")

#My Variables
ITEM_PER_PAGE=20
