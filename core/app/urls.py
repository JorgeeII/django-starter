from . import views
from django.urls import path

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
] 
