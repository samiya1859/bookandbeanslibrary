from django.urls import path
from .views import AllbookView,Comment_views,borrow_book,AddtoWishlist,wishlist
urlpatterns = [
    path('allbooks/',AllbookView,name='allbooks'),
    path('genre/<slug:gen_slug>/',AllbookView,name='genre_wise_book'),
    path('details/<int:id>/', Comment_views.as_view(), name='book_details'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow'),
    path('wishlist/',wishlist,name='wishlist'),
    path('addtowishlist/<int:id>/', AddtoWishlist,name='add_to_wishlist'),
]
