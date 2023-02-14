from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('fetch/', views.fetch, name='fetch'),
    path('details/<int:pk>/', views.details),
    path('details/<int:pk>/<str:columns>/', views.details),
]
