
from pathlib import Path
import os
from django.contrib import messages
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()
# import dj_database_url
import logging
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = env('SECRET_KEY')

DEBUG = True 
ALLOWED_HOSTS = ['*']
 
# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
    'apis',
    'core',
    'accounts',
    'courses',
    'cloudinary',
    'cloudinary_storage',

    'rest_framework',
    'rest_framework.authtoken',


    'django_password_validators',

    'whitenoise.runserver_nostatic', 
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.common.BrokenLinkEmailsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'solulearn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.getCourseCategories',
                'core.context_processors.generic_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'solulearn.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# database_config = dj_database_url.parse(os.getenv("POSTGRES_URL"))
# DATABASES = {
#     'default': database_config
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
             'min_length_digit': 2,
             'min_length_alpha': 2,
             'min_length_special': 0,
             'min_length_lower': 3,
             'min_length_upper': 0,
             'special_characters': "~!@#$%^&*()_+{}\":;'[]"
         }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_TZ = True

LOGIN_URL = '/accounts/auth/signin'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL= env('EMAIL_HOST_USER')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

AUTH_USER_MODEL = 'accounts.Profile'

MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME':env('CLOUD_STORAGE_NAME'),
    'API_KEY':env('CLOUD_STORAGE_API_KEY'),
    'API_SECRET':env('CLOUD_STORAGE_API_SECRET'),
}

# if not DEBUG:
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


AUTHENTICATION_BACKENDS = [
        # 'accounts.backends.EmailBackend',
        'rest_framework.authentication.TokenAuthentication',
        'django.contrib.auth.backends.ModelBackend',

        ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        ]
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
    'console': {
        'level': 'ERROR',
        'class': 'logging.StreamHandler',  # Output to console
    },
    'file': {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': os.path.join(BASE_DIR, 'error.log'),
    },
},
'loggers': {
    'django': {
        'handlers': ['console', 'file'],  # Output to both console and file
        'level': 'DEBUG',
        'propagate': True,
    },
},

}
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



