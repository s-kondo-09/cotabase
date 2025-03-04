from django.db import models
from .consts import MAX_RATE, CATEGORY

RATE_CHOICE = [(x, str(x)) for x in range(0, MAX_RATE + 1)]

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default="誰か")
    publisher = models.CharField(max_length=100, default="どこか")
    category = models.CharField(max_length=100, choices = CATEGORY)
    text = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Answer(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    page = models.IntegerField()
    problem_num = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    answer = models.TextField()

    def __str__(self):
        return self.title

