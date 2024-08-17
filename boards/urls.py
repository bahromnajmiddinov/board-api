from django.urls import path

from . import views


urlpatterns = [
    path('', views.BoardAPIView.as_view(), name='board-list'),
    path('<int:pk>/', views.BoardDetailAPIView.as_view(), name='board-detail'),
    path('projects/', views.ProjectAPIView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/<int:board_id>/add/', views.add_board_to_project, name='add-board-to-project'),
    
    path('star/<int:board_id>/', views.star_board, name='star-board'),
]

