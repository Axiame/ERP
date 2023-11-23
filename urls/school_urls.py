from django.urls import path
from views import school_views
urlpatterns = [
    path('schools/',views.list_schools, name='list_schools'),
    path('schools/<int:pk>/', views.retrieve_school, name='retrieve_school'),
    path('schools/create/', views.create_school, name='create_school'),
    path('schools/<int:pk>/update/', views.update_school, name='update_school'),
    path('schools/<int:pk>/delete/', views.delete_school, name='delete_school'),
]