from django.urls import path

from . import views


urlpatterns = [
    path('', views.TeamAPIView.as_view(), name='team-list'),
    path('<int:pk>/', views.TeamDetailAPIView.as_view(), name='team-detail'),
]
