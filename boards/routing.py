from django.urls import path

from . import consumers


ASGI_urlpatterns = [
    path('ws/board/<str:board_id>/', consumers.BoardConsumer.as_asgi()),
]
