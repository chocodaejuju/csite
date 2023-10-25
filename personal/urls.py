from django.urls import path
from personal import views
from community.views.base_views import detail
app_name = 'personal'

urlpatterns = [
    path('', views.index, name = 'index'),

    path('design/', views.design, name='design'),

    path('info/', views.info, name = 'info'),
    path('info/activity/', views.activity, name = 'activity'),
    path('info/activity/free/', views.activity_free, name = 'activity_free'),
    path('info/activity/tip/', views.activity_tip, name = 'activity_tip'),
    path('info/activity/shop/', views.activity_shop, name = 'activity_shop'),

    path('note/', views.note_index, name='note'),
    path('note/<int:note_id>/',
         views.note_detail, name='note_detail'),

    path('note/create/',
         views.note_create, name='note_create'),
    path('note/modify/<int:note_id>/',
         views.note_modify, name='note_modify'),
    path('note/delete/<int:note_id>/',
         views.note_delete, name='note_delete'),

    path('material/', views.material, name='material'),
    path('material/<int:material_id>/',
         views.material_detail, name='material_detail'),
    path('material/create/',
         views.material_create, name='material_create'),
    path('material/modify/<int:material_id>/',
         views.material_modify, name='material_modify'),
    path('material/delete/<int:material_id>/',
         views.material_delete, name='material_delete'),
]