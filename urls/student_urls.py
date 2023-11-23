from django.urls import path
from .views import create_student, list_students, retrieve_student, update_student, delete_student

urlpatterns = [
    path('students/', list_students, name='list_students'),
    path('students/create/', create_student, name='create_student'),
    path('students/<int:pk>/', retrieve_student, name='retrieve_student'),
    path('students/<int:pk>/update/', update_student, name='update_student'),
    path('students/<int:pk>/delete/', delete_student, name='delete_student'),
]
