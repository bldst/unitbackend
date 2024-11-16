from django.urls import path, re_path
from . import views

urlpatterns = [
    path('get_subscription/', views.get_subscription),
]
