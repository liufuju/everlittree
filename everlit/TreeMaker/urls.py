from django.urls import path, re_path
from TreeMaker import views
from django.views.generic import RedirectView
import re

urlpatterns = [
    # 这里处理的是经过everlit下的urls.p处理之后剩余的字符串，所以写的是''
    path('', views.tree_maker_main, name='treemaker'),
    path('info_file/', views.info_file, name='info_file'),
    path('info_file/create_note_cate/', views.create_note_cate, name='create_note'),
    path('create_note_cate/', views.back_your_home),
    path('info_file/info_file/', views.back_your_home)
]