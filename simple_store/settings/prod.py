from .base import *

DEBUG = False

# AWS S3 settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "sstore-static"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_LOCATION = "static"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# for storing uploaded files like images, docs and others
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "simple_store.apps.core.storage_backends.MediaStorage"

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
