from django.urls import path
from .views import comparison_view

urlpatterns = [
    path("comparison/", comparison_view),
]
