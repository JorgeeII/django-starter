from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.shortcuts import render

import json

# Authentication
class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
# Error Handling
class ErrorView(View):
    template_name = 'error_pages/error_template.html'
    status_code = None
    error_message = ''

    def get(self, request, *args, **kwargs):
        status_message, error_message = self.messages()
        return render(request, self.template_name, {'error_message': error_message, 'status_message': status_message, 'status': self.status_code}, status=self.status_code)

    def messages(self):
        status_messages = {
            403: 'Forbidden content',
            404: 'Page not found',
            500: 'Internal server error', 
        }
        error_messages = {
            403: 'We are sorry but the you don\'t have permission to view content on this page',
            404: 'We are sorry but the page you are looking for was not found',
            500: 'We are sorry but our server encountered an internal error', 
        }
        return status_messages.get(self.status_code, None), error_messages.get(self.status_code, None)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chart_data"] = self.chart_data()
        return context
    
    def chart_data(self):
        data = [
            {"x": "Category 1", "y": 55},
            {"x": "Category 2", "y": 38},
            {"x": "Category 3", "y": 62},
        ]
        return json.dumps(data)

