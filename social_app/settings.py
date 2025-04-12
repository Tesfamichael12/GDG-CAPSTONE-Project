
from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')  # Use environment variable for production

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']  # Add your domain/IP for production


# Custom User Model
AUTH_USER_MODEL = 'accounts.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',	
    'rest_framework_simplejwt.token_blacklist',
    'accounts',
    'django_extensions',  # Optional, can be excluded in production
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_app.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'social_app.wsgi.application'


# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',  # Remove or comment this line
        'rest_framework.permissions.AllowAny',  # Allow access by default
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# Database
# SQLite for development, change for production (e.g., PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Change to PostgreSQL or another DB for production
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# JWT Authentication settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_TOKEN_CHECKS': ['refresh'],
}


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# For production: You might want to serve static files via a CDN or cloud storage.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True if not DEBUG else False  # Only True for production
SESSION_COOKIE_SECURE = True if not DEBUG else False  # Only True for production
SECURE_SSL_REDIRECT = True if not DEBUG else False  # Redirect all HTTP to HTTPS in production
X_FRAME_OPTIONS = 'DENY'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# For production, set the following settings:
if not DEBUG:
    # Database settings for production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

    # Enable these settings for production
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS in production

    # Secure the secret key by setting it from an environment variable
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')



