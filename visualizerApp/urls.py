from django.urls import path
from . import views

urlpatterns = [
    path('', views.projectile_view, name='projectile'),
]