from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_by_subject'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'), 
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('<slug:slug>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<slug:slug>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('module/<int:module_id>/lesson/create/', views.LessonCreateView.as_view(), name='lesson_create'),
]