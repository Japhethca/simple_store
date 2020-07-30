from django.urls import path
from django.views.generic import TemplateView

from .views import home


urlpatterns = [path("", TemplateView.as_view(template_name="store/base.html"))]

