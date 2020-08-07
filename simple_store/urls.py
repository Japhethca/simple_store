from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("simple_store.apps.store.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/v1/", include("simple_store.apps.rest.urls")),
]
