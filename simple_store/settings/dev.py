from .base import *


# Settings Override
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, "media")
