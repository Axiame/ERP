from django.urls import path
from .views import list_classrooms, retrieve_classroom, create_classroom, update_classroom, delete_classroom

urlpatterns = [
    path('classrooms/', list_classrooms, name='list_classrooms'),
    path('classrooms/<int:pk>/', retrieve_classroom, name='retrieve_classroom'),
    path('classrooms/create/', create_classroom, name='create_classroom'),
    path('classrooms/<int:pk>/update/', update_classroom, name='update_classroom'),
    path('classrooms/<int:pk>/delete/', delete_classroom, name='delete_classroom'),
]
