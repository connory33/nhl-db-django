from django.urls import path
from . import views

urlpatterns = [
    path('api/players/', views.PlayerListView.as_view(), name='player-list'),
]