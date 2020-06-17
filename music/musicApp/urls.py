from django.conf.urls import url 
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$',views.index,name = 'index'),
    path('recommendMusic/', views.get_recommend_music, name='get_recommend_music'),
    path('updateList/', views.update_list, name='update_list'),
]