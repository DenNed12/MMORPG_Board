from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.
User = settings.AUTH_USER_MODEL

class Post(models.Model):
    author =  models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=40, null=False)
    date_time = models.DateTimeField(auto_now_add=True)
    CATCHOICES = {
        'HL': 'Хилы',
        'DD': 'ДД',
        'TR': 'Торговцы',
        'GD': 'Гилдмастеры',
        "QG": 'Квестгиверы',
        "FG": 'Кузнецы',
        "LT": "Кожевники",
        "PM": "Зельевары",
        "SM": "Мастера заклинаний"

    }
    cat = models.CharField(default='None', max_length=10, choices=CATCHOICES)
    text = models.TextField(max_length=1000, default='Текст поста')
    content = models.FileField(null=True, blank=True)


    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'



class Reply(models.Model):
    postReply = models.ForeignKey(Post, on_delete=models.CASCADE)
    authorReply = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='Текст комментария')
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} Отзыв {self.text} '

    def get_absolute_url(self):
        return reverse(viewname='post_detail', kwargs={'pk': self.post_id})

