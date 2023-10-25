from django.urls import path
from map import views

app_name = 'map'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('marker/create/', views.marker_create, name='marker_create'),
    path('marker/modify/', views.marker_modify, name='marker_modify'),
    path('marker/delete/', views.marker_delete, name='marker_delete'),
]