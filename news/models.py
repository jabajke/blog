from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс статьи', max_length=250, db_index=True)
    full_text = models.TextField('Текст статьи')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username
