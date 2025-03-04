from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import Book, Review, Answer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE

def index_view(request):
    object_list = Book.objects.order_by('-id')
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')

    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(request, 'bookapp/index.html', {'object_list': object_list, 'ranking_list': ranking_list, 'page_obj': page_obj})

class ListBookView(LoginRequiredMixin, ListView):
    template_name = 'bookapp/book_list.html'
    model = Book
    paginate_by = ITEM_PER_PAGE

class DetailBookView(LoginRequiredMixin, DetailView):
    template_name = 'bookapp/book_detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = self.object.answer_set.all().order_by('page')
        return context

class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = 'bookapp/book_create.html'
    model = Book
    fields = ('title', 'author', 'publisher', 'category', 'text', 'thumbnail')
    success_url = reverse_lazy('list-book')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'bookapp/book_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj

class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = 'bookapp/book_update.html'
    model = Book
    fields = ('title', 'author', 'publisher', 'category', 'text', 'thumbnail')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.id})
    
class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('book', 'title', 'text', 'rate')
    template_name = 'bookapp/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.book.id})

class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ('book', 'page', 'problem_num', 'title', 'answer')
    template_name = 'bookapp/answer_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.book.id})
    