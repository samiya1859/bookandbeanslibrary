from typing import Any
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView
from users.forms import ContactForm
from django.contrib import messages
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class aboutView(TemplateView):
    template_name= 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        messages.success(self.request, 'Your message has been sent successfully!')

        return redirect('home')
    

    



