
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('graph/', views.graph_view, name='graph'),
]