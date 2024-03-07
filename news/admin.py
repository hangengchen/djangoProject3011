from django.contrib import admin
from .models import Story
from .models import Author

admin.site.register(Story)
admin.site.register(Author)
