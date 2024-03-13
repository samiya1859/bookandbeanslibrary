from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True)
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    genre = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20,unique=True,null=True,blank=True)

    def __str__(self):
        return self.genre

    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='book/media/')
    borrowing_price = models.DecimalField(max_digits=10,decimal_places=2)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    Publication_date = models.DateTimeField()
    quantity = models.IntegerField()
    is_borrowed = models.BooleanField(default=False,null=True,blank=True)
    availability_status = models.BooleanField(default=True)
    is_returned = models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=20)
    review = models.TextField()
    reviewDate = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Reviewd by {self.name}"
    



class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='borrows')
    

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

    
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

