from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Articles, Comment
from .forms import ArticlesForm, CommentForm
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView


class AdminPassTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def news_home(request):
    news = Articles.objects.all().order_by
    return render(request, 'news/news_home.html', {'news': news})


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects\
            .filter(article_id=self.kwargs['pk'])\
            .order_by('-created_at')
        return context


class NewsUpdateView(AdminPassTestMixin, UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm


class NewsDeleteView(AdminPassTestMixin, DeleteView):
    model = Articles
    template_name = 'news/news_delete.html'
    success_url = '/news'


class ArticleCreateView(AdminPassTestMixin, CreateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm
    success_url = '/news'


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'news/comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_news', kwargs={'pk': self.kwargs['pk']})
