
from django.urls import path
from . import views
from .views import get_data
from .views import download_excel

urlpatterns = [
    path('', views.home, name='home'),
    path('graph/', views.graph_view, name='graph'),
    path('data/', get_data, name='data'),
     path("download-excel/", views.download_excel, name="download_excel"),
]

