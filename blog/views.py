from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Список наших блогов'
    }


class BlogCreateView(CreateView):
    model = Blog
    fields = ['topic', 'content', 'preview', ]
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Создание блога'
    }


class BlogUpdateView(CreateView):
    model = Blog
    fields = ['content', 'preview', ]
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Изменить блог'
    }


class BlogDeleteView(DeleteView):
    model = Blog
    extra_context = {
        'title': 'Удаление блога'
    }
