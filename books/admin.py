from django.contrib import admin
from .models import Book,Genre,Author,Borrow,Review
# Register your models here.
admin.site.register(Book),
admin.site.register(Genre),
admin.site.register(Author),
admin.site.register(Borrow),
admin.site.register(Review),
