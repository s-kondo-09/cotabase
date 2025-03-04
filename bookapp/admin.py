from django.contrib import admin
from .models import Book, Review, Answer

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Answer)