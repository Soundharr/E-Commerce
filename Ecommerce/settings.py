import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Django settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # Default for development; change for production
DEBUG = os.getenv('DEBUG', 'True') == 'True'
#ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1', 'https://soundhar-e-commerceshopping.netlify.app/').split(',')

ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,soundhar-e-commerceshopping.netlify.app'
).split(',')


# Applications installed in the Django project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products', # product app
    'shopping', # shopping app
    'register', # register app
    'rest_framework',
    'corsheaders',
    'storages',
    'cloudinary',
    'cloudinary_storage',
]

# Middleware for handling requests
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

# Root URL configuration
ROOT_URLCONF = 'Ecommerce.urls'

# Templates settings
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

# WSGI application to use for deployment
WSGI_APPLICATION = 'Ecommerce.wsgi.application'

# Database configuration
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

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (images, documents, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Storage configuration (local for development or Cloudinary for production)
DEFAULT_FILE_STORAGE = (
    'django.core.files.storage.FileSystemStorage'
    if DEBUG else
    'cloudinary_storage.storage.MediaCloudinaryStorage'
)

# Cloudinary configuration for media storage (production)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', 'your-cloud-name'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', 'your-api-key'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', 'your-api-secret'),
}

# Allowed origins for cross-origin requests
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Adjust this according to your frontend
    "http://127.0.0.1:5173",
    "https://yourfrontenddomain.com",  # Replace with your deployed frontend domain
    "https://soundhar-e-commerceshopping.netlify.app",
    "https://soundharr.github.io",
]
 # Replace with your deployed frontend domain

# Rest framework configuration for APIs
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# Default auto field for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Secure headers for proxies in production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Whitenoise auto-refresh for static files (useful in development)
WHITENOISE_AUTOREFRESH = DEBUG

# Add any other settings you might need here...
# === MailerSend SMTP settings ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailersend.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'MS_Ub08uE@test-p7kx4xwd7xvg9yjr.mlsender.net'
EMAIL_HOST_PASSWORD = 'mssp.MB1ltQ7.x2p034733w7gzdrn.H6EPXnA'

# ❗IMPORTANT: Must match a verified sender in MailerSend
DEFAULT_FROM_EMAIL = 'MS_Ub08uE@test-p7kx4xwd7xvg9yjr.mlsender.net'

# Optional: Twilio setup (disabled unless used)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')