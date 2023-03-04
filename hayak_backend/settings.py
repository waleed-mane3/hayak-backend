# IMPORTS ###################################################################
import os, environ, socket
from pathlib import Path
from datetime import timedelta




# CONSTANTS #################################################################
ADMIN=1
CLIENT=2
STAFF=3




# BASE DIR ##################################################################
BASE_DIR = Path(__file__).resolve().parent.parent
root_path = environ.Path(__file__)
file_path = os.path.join(BASE_DIR, "hayak_backend/.env")
env = environ.Env()
environ.Env.read_env(file_path)




# SECURITY ##################################################################
SECRET_KEY = env('SECRET_KEY')
CORS_ORIGIN_ALLOW_ALL=True
###############################
def get_ec2_instance_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip

AWS_LOCAL_IP = get_ec2_instance_ip()
DEBUG = env('DEBUG', default= False)
ALLOWED_HOSTS = [
        env('APP_URL'), 
        env('HOST_URL'),
        AWS_LOCAL_IP,
        '127.0.0.1',
        '81ff-31-166-186-157.ngrok.io'
    ]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "POST",
    "PUT",
]
# # CSRF verification for admin panel -----------------------       ##
TRUSTED_ORIGIN = []
for host in ALLOWED_HOSTS:
    TRUSTED_ORIGIN.append(''.join(('https://', host)))
CSRF_TRUSTED_ORIGINS = TRUSTED_ORIGIN
CSRF_TRUSTED_ORIGINS.append('http://127.0.0.1')
# CSRF verification for admin panel -----------------------




# SECURITY #####################################################################
# SECRET_KEY = 'django-insecure-g4@!&)+ds#+zw0*%93%5(x(8c*760zim&@pxc8j*8y5m$@3*e3'
# DEBUG = True
# ALLOWED_HOSTS = ["*", "64d1-31-166-129-65.ngrok.io"]




# APPLICATIONS #################################################################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps 
    'auth_system',
    'account',
    'design',
    'event',
    'package',
    'scan',
    'webhook',

    # Packages 
    'rest_framework',
    'django_rest_passwordreset',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'import_export',
    'drf_yasg',
    'django_cleanup.apps.CleanupConfig',
    'storages'
]




# RDF ############################################################################
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
# JWT AUTH Settings  
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    # custom
    # https://www.procoding.org/jwt-token-as-httponly-cookie-in-django/
    # # https://stackoverflow.com/questions/66247988/how-to-store-jwt-tokens-in-httponly-cookies-with-drf-djangorestframework-simplej
    # 'AUTH_COOKIE': 'access',  # Cookie name. Enables cookies if value is set.
    # 'AUTH_COOKIE_DOMAIN': None ,#"hayak-application.herokuapp.com",     # A string like "example.com", or None for standard domain cookie.
    # 'AUTH_COOKIE_SECURE': False,    # Whether the auth cookies should be secure (https:// only).
    # 'AUTH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag.It's not fetch by javascript.
    # 'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    # 'AUTH_COOKIE_SAMESITE': None,  # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
}



# MIDDLEWARE #####################################################################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'hayak_backend.urls'
WSGI_APPLICATION = 'hayak_backend.wsgi.application'
# TEMPLATES #####################################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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




# # DATABASES ##################################################################### 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'db_h_db',
#         'USER': 'db_h_user',
#         'PASSWORD': 'hhaya_1992',
#         'HOST': 'h-identifier.culhzk21cl27.eu-west-1.rds.amazonaws.com',
#         'PORT':'5432'
#     }
# }
# DATABASE ################################################################# 
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT')
    }
}




# PASSWORD VALIDATION ############################################################
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





# INTERNATIONALIZATION ###########################################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True





# FILE STORAGE ########################################################################
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATIC_URL = '/static/'
# MEDIA_URL = '/images/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
# # S3 BUCKETS CONFIG ### 
# AWS_ACCESS_KEY_ID = 'AKIARHSDXOCNBWZA5MVO'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'hayak-buket'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# # FILE STORAGE ##############################################################
is_s3_enabled = eval(env('S3_ENABLED'))
if is_s3_enabled:
    DEFAULT_FILE_STORAGE = 'hayak_backend.storage_backends.MediaStorage'
    STATICFILES_STORAGE = 'hayak_backend.storage_backends.StaticStorage'
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='eu-west-1')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = env('AWS_LOCATION')
    AWS_LOCATION_MEDIA = env('AWS_LOCATION_MEDIA')
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION_MEDIA)
else:
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='eu-west-1')
    # AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'




# MISCELLANEOUS ##################################################################
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'auth_system.CustomUser'
IMPORT_EXPORT_USE_TRANSACTIONS = True 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'































# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = [
#         'accept',
#         'accept-encoding',
#         'authorization',
#         'content-type',
#         'dnt',
#         'origin',
#         'user-agent',
#         'x-csrftoken',
#         'x-requested-with',
# ]
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_DOMAIN = 'example.com'
# https://stackoverflow.com/questions/53052611/ajax-call-with-withcredentials-true-is-not-sending-cookie-in-request ##
# SESSION_COOKIE_SAMESITE = None