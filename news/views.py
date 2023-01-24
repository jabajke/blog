from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic

from .models import Articles, Comment
from .forms import ArticlesForm, CommentForm


def news_home(request):
    news = Articles.objects.all().order_by
    return render(request, 'news/news_home.html', {'news': news})


class NewsDetailView(generic.DetailView):
    model = Articles
    template_name = 'news/detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article_id=self.kwargs['pk'])
        return context


class NewsUpdateView(generic.UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm


class NewsDeleteView(generic.DeleteView):
    model = Articles
    template_name = 'news/news_delete.html'
    success_url = '/news'


class ArticleCreateView(generic.CreateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm
    success_url = '/news'


class CommentCreateView(generic.CreateView):
    model = Comment
    template_name = 'news/comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_news', kwargs={'pk': self.kwargs['pk']})
