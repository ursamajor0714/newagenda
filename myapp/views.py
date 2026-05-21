from django.shortcuts import render, redirect
from .models import Post, Comment, Visitor
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import CustomRegisterForm 
from django.contrib.auth import login


def landing(request):
    return render(request, 'landing.html')

def home(request):
    from datetime import timedelta
    from django.utils import timezone
    query = request.GET.get('query', '')
    search_type = request.GET.get('search_type', 'title')
    search_period = request.GET.get('search_period', 'all')
    posts = Post.objects.all().order_by('-id')
    today = timezone.now().date()
    today_posts = Post.objects.filter(date__date=today).count()
    today_comments = Comment.objects.filter(date__date=today).count()
    if query:
        if search_type == 'title':
            posts = posts.filter(title__icontains=query)
        elif search_type == 'content':
            posts = posts.filter(content__icontains=query)
        elif search_type == 'title_content':
            posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)
        elif search_type == 'user':
            posts = posts.filter(user__icontains=query)

    if search_period == 'today':
        posts = posts.filter(date__date=today)
    elif search_period == 'week':
        posts = posts.filter(date__date__gte=today - timedelta(days=7))
    elif search_period == 'month':
        posts = posts.filter(date__date__gte=today - timedelta(days=30))


    paginator = Paginator(posts, 30)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    if not Visitor.objects.filter(ip=ip, date=today).exists():
        Visitor.objects.create(ip=ip)
    today_visitors = Visitor.objects.filter(date=today).count()
    return render(request, 'home.html', {
    'posts': posts,
    'today_posts': today_posts,
    'today_comments': today_comments,
    'today_visitors': today_visitors,
})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    prev_post = Post.objects.filter(id__lt=pk).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=pk).order_by('id').first()
    return render(request, 'post_detail.html', {'post': post, 
    'prev_post': prev_post,
    'next_post': next_post,
    'comments': comments,
    })

def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    session_key = f'liked_{pk}'
    if not request.session.get(session_key):
        post.likes += 1
        post.save()
        request.session[session_key] = True
    return redirect('post_detail', pk=pk)

@login_required
def hate_post(request, pk):
    post = Post.objects.get(pk=pk)
    session_key = f'hated_{pk}'
    if not request.session.get(session_key):
        post.hates +=1
        post.save()
        request.session[session_key] = True
    return redirect('post_detail', pk=pk)

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(
            post=post,
            content=content,
            user=request.user.username
        )
    return redirect('post_detail', pk=pk)

def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(
            title=title,
            content=content,
            user=request.user.username,
        )
        return redirect('home')
    return render(request, 'write.html')

def trap(request):
    return render(request, 'trap.html')

