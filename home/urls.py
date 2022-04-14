from django.urls import path
from . import views


print("home urls py")
urlpatterns = [
    path('',views.index, name='index')

]
