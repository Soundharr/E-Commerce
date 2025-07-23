from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# Load environment variables from .env
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,soundhar-e-commerceshopping.netlify.app'
).split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'products',
    'shopping',
    'register',

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'storages',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecommerce.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ecommerce'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User model
AUTH_USER_MODEL = 'register.User'

# REST Framework config

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),  # Set expiry time for access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),  # Set expiry time for refresh token
}


# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://soundhar-e-commerceshopping.netlify.app",
    "https://soundharr.github.io",
    "http://localhost:3000",
]

# Cloudinary (media storage for production)
DEFAULT_FILE_STORAGE = (
    'django.core.files.storage.FileSystemStorage'
    if DEBUG else
    'cloudinary_storage.storage.MediaCloudinaryStorage'
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', 'your-cloud-name'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', 'your-api-key'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', 'your-api-secret'),
}

# # Email settings (MailerSend)
# # settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# MailerSend SMTP Settings
EMAIL_HOST = 'smtp.mailersend.net'
EMAIL_PORT = 587  # or 2525 (both are TLS-supported)
EMAIL_USE_TLS = True  # Use TLS connection
EMAIL_HOST_USER = 'MS_Ub08uE@test-p7kx4xwd7xvg9yjr.mlsender.net'  # SMTP Username
EMAIL_HOST_PASSWORD = 'mssp.MB1ltQ7.x2p034733w7gzdrn.H6EPXnA'  # SMTP Password
DEFAULT_FROM_EMAIL = 'no-reply@yourdomain.com'  # Sender's email address (adjust this as needed)


# Twilio (optional)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

# For deployed apps behind reverse proxies (e.g., on Render)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Whitenoise auto-refresh during development
WHITENOISE_AUTOREFRESH = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mailersend.net')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)




# Email settings (MailerSend)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# # MailerSend SMTP Settings (Corrected)
# EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mailersend.net')  # Use environment variable or default to MailerSend
# EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # Use environment variable or default to 587
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'  # Ensure TLS is used by default
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'MS_Ub08uE@test-p7kx4xwd7xvg9yjr.mlsender.net')  # Use environment variable or default to your MailerSend user
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'mssp.MB1ltQ7.x2p034733w7gzdrn.H6EPXnA')  # Use environment variable or default to your MailerSend password
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@yourdomain.com')  # Use environment variable or default to 'no-reply@yourdomain.com'

# # Optional: Use console backend for local development to see email output in the console (for testing)
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# # Twilio (optional)
# TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
# TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
# TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

# # For deployed apps behind reverse proxies (e.g., on Render)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # Whitenoise auto-refresh during development
# WHITENOISE_AUTOREFRESH = DEBUG
