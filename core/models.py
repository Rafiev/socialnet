from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField('Photo', null=True, blank=False, upload_to='profile_images/')
    subscribers = models.ManyToManyField(to=User, related_name='followed_profile', blank=True)
    link_fb = models.CharField(max_length=255, null=True, blank=True)
    whatsapp = models.CharField(max_length=30, null=True, blank=True)
    telegram = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.nickname


class Post(models.Model):
    STATUS_CHOICES = (('Posted', 'Posted'),
                      ('Unposted', 'Unposted'))

    name = models.CharField('Header', max_length=80, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    photo = models.ImageField('Photo', null=True, blank=False, upload_to="post_images/")
    status = models.CharField('Status', max_length=200, choices=STATUS_CHOICES, default="Posted")
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Post author', related_name='posts')
    category = models.ManyToManyField(to='Category', blank=True, verbose_name='categories')
    likes = models.IntegerField('Like', default=0)

    def __str__(self):
        return f'{self.name} - {self.status}'


class Category(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )

    name = models.CharField(max_length=50)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, null=True, blank=True,)

    def __str__(self):
        return f'{self.name} - {self.rating}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=False)
    comment_text = models.TextField()
    likes_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text[:20]

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']


class Short(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=False,
                             verbose_name='Author', related_name='short')
    video = models.FileField('Video', upload_to='video_post/')
    created_at = models.DateTimeField(auto_now_add=True)
    views_qty = models.PositiveIntegerField('Views', default=0)
    viewed_users = models.ManyToManyField(to=User, blank=True, related_name='viewed_shorts')
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Short'
        verbose_name_plural = 'Shorts'

    def __str__(self):
        return f'{self.video} - {self.created_at}'


class SavedPosts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, verbose_name='saved post', related_name='saved_posts')

    class Meta:
        verbose_name = 'saved post'
        verbose_name_plural = 'saved posts'

    def __str__(self):
        return f'{self.user}'


class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    text = models.CharField(max_length=255)
    is_showed = models.BooleanField(default=False)

    def __str__(self):
        return self.text