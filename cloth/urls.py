from django.urls import path

from . import views

app_name = 'cloth'
# 경로 cloth/
urlpatterns = [
    path('', views.index, name = 'index'),
]