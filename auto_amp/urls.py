from django.urls import path

from .views import canonical_to_amp


urlpatterns = [path("<path:canonical_path>", canonical_to_amp)]
