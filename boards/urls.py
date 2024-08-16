from django.urls import path

from . import views


urlpatterns = [
    path('', views.BoardAPIView.as_view(), name='board-list'),
    path('<int:pk>/', views.BoardDetailAPIView.as_view(), name='board-detail'),
    path('projects/', views.ProjectAPIView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='project-detail'),
]

