"""
Django settings for collaborative project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_ROOT = os.path.join(BASE_DIR, "www/assets")
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gq301$(s^m%n*k$k#u5xw%532tj-nrn4o^26!yb-%=cmu#3swx'

# Google OAuth for Private Sheets Access
GOOGLE_CLIENT_ID = "507707897389-566t26bmm0mjsrpm6opt1m459j5esqrd.apps.googleusercontent.com"
# Not secret! We're using public client security model. This
# puts the burden on the user to explicitly grant access (via
# copy and paste into the application)
GOOGLE_CLIENT_SECRET = "Uk1AHTyOgNNTXz9EUa4Ezph7"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',

    'social_django',
    'import_export',
    'taggit',

    'django_models_from_csv',
    'collaborative',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'collaborative.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
            # TODO: figure out a way to auto import admin template overrides
            # from within the csv models module
            'django_models_from_csv/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'collaborative.wsgi.application'

CSV_MODELS_TEMP_DB = "schemabuilding"
CSV_MODELS_WIZARD_REDIRECT_TO = "/setup-auth/"
CSV_MODELS_AUTO_REGISTER_ADMIN = False

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    CSV_MODELS_TEMP_DB: {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
]

AUTHENTICATION_BACKENDS = (
    'collaborative.auth.GoogleOAuth2',
    'social_core.backends.slack.SlackOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = "/setup-check/"

# Google Sign In
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""

# Slack Sign In
SOCIAL_AUTH_SLACK_KEY = ""
SOCIAL_AUTH_SLACK_SECRET = ""
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/admin/"
SOCIAL_AUTH_SLACK_TEAM = ""

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Make sure the user is in the configured Slack team
    'collaborative.user.enforce_slack_team',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # Pause the pipeline if user isn't granted access
    # 'social_core.pipeline.social_auth.associate_by_email',
    'collaborative.user.associate_by_email_or_pause',

    # # Make up a username for this person, appends a random string at the end if
    # # there's any collision.
    # 'social_core.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # # Create a user account if we haven't found one yet.
    # 'social_core.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # # Set the user account to is_staff (else they can't use the Admin panel):
    # 'collaborative.user.set_staff_status',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',
)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# Language of the codebase
LANGUAGE_CODE = 'en-us'
# UI languages (for translation)
LANGUAGES = [
    ('es', 'Spanish'),
    ('en', 'English'),
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# The URL that static assets will get accessed via the browser
STATIC_URL = '/static/'

# Where static assets are stored for this module
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

try:
   from collaborative.settings_dev import *
except:
    pass

# Setings (OAuth, etc) from configuration wizard
# This is a stopgap until we find a better credential
# storage solution
try:
   from collaborative.settings_prod import *
except:
    pass
