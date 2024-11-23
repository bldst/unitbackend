from django.urls import path
from . import views
urlpatterns = [

    path('ceshi/', views.forwardtohpc)
]
