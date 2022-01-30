from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ngo_admin_home, name='ngo_admin_home'),
    path('profile', views.ngo_admin_profile, name='ngo_admin_profile'),
    path('update_profile', views.update_profile, name='ngo_admin_update_profile'),
    path('create_content', views.create_content, name='ngo_admin_create_content'),
    path('edit_content', views.edit_content, name='ngo_admin_edit_content'),
    path('update_content', views.update_content, name='ngo_admin_update_content'),
    path('quizboard', views.ngo_admin_quizboard, name='ngo_admin_quizboard'),
    path('create_quiz', views.create_quiz, name='ngo_admin_create_quiz'),
    path('edit_quiz', views.edit_quiz, name='ngo_admin_edit_quiz'),
    path('update_quiz', views.update_quiz, name='ngo_admin_update_quiz'),
    path('health_worker', views.ngo_admin_chw, name='ngo_admin_chw'),
    path('create_chw', views.create_chw, name='ngo_admin_create_chw'),
    path('edit_chw', views.edit_chw, name='ngo_admin_edit_chw'),
    path('update_chw', views.update_chw, name='ngo_admin_update_chw'),

    path('super_admin_home', views.super_admin_home, name="super_admin_home"),
    path('create_ngo', views.create_ngo, name="super_admin_create_ngo"),
    path('edit_ngo', views.edit_ngo, name="super_admin_edit_ngo"),
    path('update_ngo', views.update_ngo, name='ngo_admin_update_ngo'),
    path('delete_ngo/<str:pk>/', views.delete_ngo, name='ngo_admin_delete_ngo'),
    path('super_admin_ngo_member', views.super_admin_ngo_member, name="super_admin_ngo_member"),
    path('create_ngo_admin', views.create_ngo_admin, name="super_admin_create_ngo_admin"),
    path('delete_ngo_admin', views.delete_ngo_admin, name="super_admin_delete_ngo_admin"),

    path('verify_access_token', views.verify_access_token, name="verify_access_token"),
    path('get_content',views.get_content, name="get_content"),
    path('get_quiz',views.get_quiz, name="get_quiz"),
]
