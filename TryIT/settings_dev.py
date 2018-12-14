# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from TryIT.settings_global import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')k(v80b=g^sv@4c2k0!9rwpk7d%*di2sne&8eyqfi&lbb=mila'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'congress/static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



# Email
EMAIL_PORT = 2500
EMAIL_HOST = 'localhost'