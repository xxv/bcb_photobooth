DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bcb_attendees',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

################## storage

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'bcbfaces'
AWS_ACCESS_KEY_ID = '' # add me
AWS_SECRET_ACCESS_KEY = '' # add me (super-secret)

MEDIA_ROOT = '' # add me

MEDIA_URL = '/static/'

UPLOADED_MEDIA_URL = '/uploads/'

ADMIN_MEDIA_PREFIX = '/media/'

TEMPLATE_DIRS = (
    "" # add me
)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

SECRET_KEY = '' # add me

