from django.urls import path
from . import views



app_name='core'
urlpatterns = [
    path('', views.web, name= 'web'),
    path('home/', views.home, name='home'),
]
