from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.exceptions import ValidationError

from .models import Author, Story
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth import logout
from rest_framework.generics import CreateAPIView
from .serializers import StorySerializer


def stories_list(request):
    stories = Story.objects.all()  # 获取所有故事
    username = request.session.get('username', None)  # 从session获取用户名
    context = {
        'stories': stories,
        'username': username  # 添加用户名到上下文
    }
    return render(request, 'index.html', context)


def story_detail(request, story_id):
    # 获取故事实例，如果不存在则返回404
    story = get_object_or_404(Story, pk=story_id)
    username = request.session.get('username', None)  # 从session获取用户名
    context = {
        'username': username,  # 添加用户名到上下文
        'story': story
    }
    return render(request, 'blog-details.html', context)


def login_page(request):
    return render(request, 'login.html')


def post_page(request):
    username = request.session.get('username', None)  # 从session获取用户名
    context = {
        'username': username  # 添加用户名到上下文
    }
    return render(request, 'post_story.html', context)


@csrf_exempt  # 允许跨站请求
def login_view(request):
    if request.method == 'POST':
        # 从POST请求中获取用户名和密码
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 验证用户名和密码是否与Author表中的记录匹配
        try:
            name = Author.objects.get(name=name)
            author = Author.objects.get(username=username)
            if author.password == password:
                # 如果用户名和密码匹配，重定向到主界面
                request.session['username'] = author.username
                return HttpResponseRedirect(reverse('stories-list'))  # 假设你有一个名为'index'的URL pattern
            else:
                # 如果密码不匹配，返回错误信息
                return HttpResponse("Invalid password.", content_type="text/plain", status=400)
        except Author.DoesNotExist:
            # 如果用户名不存在，返回错误信息
            return HttpResponse("Invalid username.", content_type="text/plain", status=400)
    else:
        # 如果请求方法不是POST，返回错误信息
        return HttpResponse("Login only supports POST method.", content_type="text/plain", status=405)


# views.py

@csrf_exempt  # 允许跨站请求
def logout_view(request):
    if request.method == 'POST':
        if 'username' in request.session:
            logout(request)
            request.session.flush()
            return HttpResponseRedirect(reverse('stories-list'))  # 使用reverse函数来重定向到首页视图
        else:
            return HttpResponse("No user is logged in.", content_type="text/plain", status=400)
    else:
        return HttpResponse("Logout only supports POST method.", content_type="text/plain", status=405)


class StoryCreateAPIView(CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 从session中获取author的username
        author_username = self.request.session.get('username')
        if author_username:
            # 根据username获取Author实例
            try:
                author = Author.objects.get(username=author_username)
                serializer.save(author=author)
                # return HttpResponseRedirect(reverse('index'))
            except Author.DoesNotExist:
                # 如果没有找到Author，您可以抛出异常或返回错误
                raise ValidationError('Author does not exist.')
        else:
            # 如果session中没有username，您可以抛出异常或返回错误
            raise ValidationError('No author found in session.')


@csrf_exempt
def delete_story(request, key):
    try:
        story = get_object_or_404(Story, pk=key)
        story.delete()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e, status=503)
