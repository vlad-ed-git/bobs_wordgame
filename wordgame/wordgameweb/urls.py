from django.contrib import admin
from django.urls import path
from . import views

#register namespace
app_name = 'wordgameweb'
urlpatterns = [
    path('' , views.login , name="login" ),
    path('' , views.home , name="home" ),
]
