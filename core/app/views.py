from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


