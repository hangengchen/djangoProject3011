from django.urls import path
from . import views
from .views import login_page, logout_view, StoryCreateAPIView, post_page, stories_list, story_detail, delete_story

urlpatterns = [
    path('', stories_list, name='stories-list'),
    # path('', index, name='index'),
    path('api/login', views.login_view, name='login'),
    path('login/', login_page, name='login_page'),
    path('api/logout', logout_view, name='logout'),
    path('api/stories', StoryCreateAPIView.as_view(), name='api-create-story'),
    path('post/', post_page, name='post_page'),
    path('blog_detail/<int:story_id>/', story_detail, name='story-detail'),
    path('api/stories/<int:key>/', delete_story, name='delete-story'),
]
