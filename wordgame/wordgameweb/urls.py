from django.contrib import admin
from django.urls import path
from . import views

#register namespace
app_name = 'wordgameweb'
urlpatterns = [
    path('' , views.signIn , name="login" ),
    path('home/' , views.home , name="home" ),
    path('create-list/' , views.create_list, name="create-list"),
    path('edit-list/<int:list_number>/', views.editList , name="edit-list"),
    path('view-word/<int:word_id>/<int:list_number>/', views.viewWord , name="view-word")
]
