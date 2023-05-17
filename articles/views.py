from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView
)
from django.urls import reverse_lazy
# from jinja2 import Template
from .models import Article


class ArticleListView(ListView):
    queryset = Article.objects.order_by('-id')
    model = Article
    template_name = 'articles/article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    success_url = reverse_lazy('article_list')


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo')
    template_name = 'articles/articles_update.html'

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'articles/article_create.html'
    fields = ('title', 'summary', 'body', 'photo')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
