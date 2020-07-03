from django.urls import path
from . import views



app_name='core'
urlpatterns = [
    path('', views.web, name= 'web'),
    path('search', views.search, name= 'search'),
    path('home/search', views.search, name= 'search2'),
    path('home/', views.home, name='home'),
]
