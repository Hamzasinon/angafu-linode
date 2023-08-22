from django.urls import path
from . import views
# ######:8000/angaapp

urlpatterns = [
    path('',views.simple_view ),
]