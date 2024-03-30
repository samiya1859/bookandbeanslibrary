from django.urls import path
from .views import SignupView, activate, UserLoginView,logOut, Profileview, edit_profile, pass_change,borrow_history,WriteReview,return_book,ReturnBookView,wishlist_history

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/',logOut, name='logout'),
    path('profile/<int:id>/', Profileview.as_view(), name='profile'),
    path('profile/borrowhis/',borrow_history,name='borrow_history'),
    path('profile/wishhis/',wishlist_history,name='wish_history'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('pass_change/', pass_change, name='pass_change'),
    path('write_review/<int:id>/', WriteReview.as_view(), name='write_review'),
    path('return/<int:id>/', ReturnBookView.as_view(), name='return'),
    
]
