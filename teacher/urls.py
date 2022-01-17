from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ngo_admin_home, name='ngo_admin_home'),
    path('create_content', views.create_content, name='ngo_admin_create_content'),
    path('edit_content', views.edit_content, name='ngo_admin_edit_content'),
    path('update_content', views.update_content, name='ngo_admin_update_content'),
    path('health_worker', views.ngo_admin_chw, name='ngo_admin_chw'),
    path('create_chw', views.create_chw, name='ngo_admin_create_chw'),
    path('edit_chw', views.edit_chw, name='ngo_admin_edit_chw'),
    path('update_chw', views.update_chw, name='ngo_admin_update_chw'),
    path('committee', views.teacher_committee, name='teacher_committee'),
    path('head', views.teacher_head, name='teacher_head'),
    path('create_course', views.create_course, name='teacher_create_course'),
    path('create_deadline', views.create_deadline, name='teacher_create_deadline'),
    path('create_committee', views.create_committee, name='teacher_create_committee'),
    path('edit_deadlines', views.edit_deadline, name="committee_edit_deadline"),

    # path('createsession/', views.createsession, name='createsession'),
    # path('<str:session_id>/', views.batchinfo, name='batchinfo'),
    # path('<str:session_id>/<str:project_id>/', views.projectdetails, name='projectdetails'),
]
