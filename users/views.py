from django.shortcuts import render,redirect,get_object_or_404
from . import forms
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,DeleteView,View
from django.contrib.auth.forms import AuthenticationForm ,PasswordChangeForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
import binascii
from django.views.generic import DetailView
from .forms import ChangeUserForm
from books.models import Borrow,Review,Book
from books.forms import ReviewForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        messages.success(self.request, 'Please Check your Account and Active Your Account')
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('confirmationmail.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
})

        to_email = form.cleaned_data.get('email')
        email = EmailMultiAlternatives(subject, message, to=[to_email])
        email.send()

        return redirect('login')
       
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.warning(self.request, 'SignUp in information incorrect')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context


def activate(request, uidb64, token):
    print(uidb64)
    users = User.objects.get(pk=uidb64)
    users.is_active = True
    users.save()
    return redirect('login')

class UserLoginView(LoginView):
    template_name ='login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successfully')
        return super().form_valid(form)
    
    
    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        messages.warning(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    

def logOut(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

class Profileview(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'id'

def edit_profile(request):
    if request.method == 'POST':
        profile_form = ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('edit_profile')
    
    else:
        profile_form = ChangeUserForm(instance = request.user)
    return render(request, 'editprofile.html', {'form' : profile_form})

def pass_change(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password Updated successfully!')
            return redirect('profile')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'passChange.html',{'form':form})

def borrow_history(request):
    
    borrowed_books = Borrow.objects.filter(user = request.user)
    
    return render(request, 'borrowlist.html', {'borrowed_books': borrowed_books})


def return_book(request, id):
    print('return book func ', id)
    
    book = get_object_or_404(Book, pk=id)

    
    return redirect('allbooks')

class ReturnBookView(View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)

        if book.is_borrowed:
            
            form = ReviewForm()
            return render(request, 'writereview.html', {'book': book, 'form': form})
        else:
            messages.error(request, 'This book has not been borrowed.')
            return redirect('allbooks')

    def post(self, request, id):
        book = get_object_or_404(Book, id=id)

        if book.is_borrowed:
            form = ReviewForm(request.POST)
            if form.is_valid():
                # Save the review
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                
                book.quantity += 1
                book.is_borrowed = False
                book.save()

                messages.success(request, 'Review submitted successfully. Book returned.')
                return redirect('allbooks')
            else:
                messages.error(request, 'Invalid review. Please try again.')
                return render(request, 'writereview.html', {'book': book, 'form': form})
        else:
            messages.error(request, 'This book has not been borrowed.')
            return redirect('allbooks')



class WriteReview(CreateView):
    template_name = 'writereview.html'
    form_class = ReviewForm
    success_url = reverse_lazy('allbooks')  
    def form_valid(self, form):
        form.instance.book_id = self.kwargs['book_id'] 
        form.instance.user = self.request.user  
        
        return super().form_valid(form)