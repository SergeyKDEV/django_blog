from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Post, Category
from django.utils import timezone

DISPLAY_POSTS_COUNT = 10


def index(request):
    """
    Главная страница проекта.
    """
    post_list = Post.objects.filter(
        Q(pub_date__lte=timezone.now())
        & Q(is_published=True)
        & Q(category__is_published=True)
    ).order_by('pub_date')[:DISPLAY_POSTS_COUNT]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """
    Страница категории.
    """
    post = get_object_or_404(Post.objects.exclude(
        Q(pub_date__gt=timezone.now())
        | Q(is_published=False)
        | Q(category__is_published=False)
    ), id=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """
    Страница отдельной публикации.
    """
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True
        ), slug=category_slug)
    post_list = Post.objects.filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True)
    context = {'category': category,
               'post_list': post_list}
    return render(request, 'blog/category.html', context)
