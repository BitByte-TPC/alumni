from AluminiConnect.settings.common import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY_ALUMNI")

DEBUG = False

ALLOWED_HOSTS = ['58.84.25.100', '103.59.142.75', 'https://www.iiitdmj.ac.in/sac.iiitdmj.ac.in/', 'sac.iiitdmj.ac.in']

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static/')
