from django.urls import path
from . import views


urlpatterns = [
    path('',views.drivers, name='drivers'),
    path('takeadonation/',views.takeadonation, name='takeadonation')
]