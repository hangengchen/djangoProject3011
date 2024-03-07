from django.db import models

# from django.contrib.auth.models import User

# 选择列表用于新闻故事的类别
CATEGORY_CHOICES = [
    ('pol', 'Politics'),
    ('art', 'Art'),
    ('tech', 'Technology'),
    ('trivia', 'Trivia'),
]

# 选择列表用于新闻故事的地区
REGION_CHOICES = [
    ('uk', 'United Kingdom'),
    ('eu', 'European'),
    ('w', 'World'),
]


class Author(models.Model):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)  # 密码通常需要使用更安全的方式处理，比如使用Django的User模型

    def __str__(self):
        return self.name


class Story(models.Model):
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline
