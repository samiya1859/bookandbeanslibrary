from django.shortcuts import render,redirect,get_object_or_404
from .models import Book,Borrow,Review,Genre,WishlistItem
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView,TemplateView
from .forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
def AllbookView(request, gen_slug=None):
    data = Book.objects.all()
    genres = Genre.objects.all()
    genre = None
    

    if gen_slug:
        genre = get_object_or_404(Genre, slug=gen_slug)
        data = Book.objects.filter(genre=genre)

    return render(request, 'allbooks.html', {'data': data, 'genre': genre, 'genres': genres})

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'
    

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            book = self.get_object()
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully.')
        else:
            messages.error(request, 'Error adding review.')

        book_id = kwargs.get('book_id')
        return redirect(reverse('book_details', kwargs={'book_id': book_id}))

class Comment_views(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'
 
    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()
        return self.get(request, *args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        context['reviews']=reviews
        return context



def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.quantity > 0:
        # Create a Borrow object for the current user and book
        Borrow.objects.create(user=request.user, book=book)

        # Decrease the quantity of the book by 1
        book.quantity -= 1
        book.is_borrowed=True
        book.save()

        messages.success(request, 'Book borrowed successfully!')
    else:
        messages.error(request, 'Sorry, this book is not available for borrowing.')

    return redirect('allbooks')

 

def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def AddtoWishlist(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id)
        if book.quantity == 0:
            WishlistItem.objects.create(user=request.user, book=book)
            messages.success(request, 'Book added to wishlist successfully.')
        else:
            messages.error(request, 'This book is currently available. You can borrow it instead of adding to wishlist.')
        return redirect('allbooks')
    else:
        return redirect('allbooks') 



class ReturnBook(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        borrow_id = kwargs.get('borrow_id')
        borrow = get_object_or_404(Borrow, pk=borrow_id)

        if borrow.user == request.user:
            book = borrow.book
            book.quantity += 1  
            book.save()

            borrow.delete() 

            messages.success(request, 'Book returned successfully!')
        else:
            messages.error(request, 'You are not authorized to return this book.')

        return redirect('wishlist')  
