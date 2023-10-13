from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic import (ListView,
                                  DetailView,
                                  UpdateView,
                                  CreateView,
                                  DeleteView)
from .models import Post, Category, User, Comment
from .forms import PostForm, CommentForm, UserForm

DISPLAY_POSTS_COUNT = 10


class IndexListView(ListView):
    """
    Главная страница проекта.
    """
    model = Post
    template_name = 'blog/index.html'
    paginate_by = DISPLAY_POSTS_COUNT

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comment')
        )


class PostDetail(DetailView):
    """
    Страница отдельной записи.
    """
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.select_related(
            'author'
        )
        return context


class CategoryPage(ListView):
    """
    Страница отдельной категории.
    """
    model = Post
    template_name = 'blog/category.html'
    paginate_by = DISPLAY_POSTS_COUNT

    def get_queryset(self):
        slug = self.kwargs['category_slug']
        self.category = get_object_or_404(
            Category,
            slug=slug,
            is_published=True
        )
        return super().get_queryset().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
            category=self.category
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class EditPost(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирование поста.
    """
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('blog:post_detail', self.get_object().pk)
        get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.object.pk}
                            )


class DeletePost(LoginRequiredMixin, DeleteView):
    """
    Удаление поста.
    """
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'
    login_url = '/auth/login/'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user,
            pk=self.kwargs['post_id']
        )

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.author != self.request.user:
            raise PermissionDenied
        return post


class UserProfileDetail(ListView):
    """
    Страница профиля пользователя.
    """
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    paginate_by = DISPLAY_POSTS_COUNT

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            author=get_object_or_404(User, username=self.kwargs['username']),
            is_published=True,
            category__is_published=True
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comment')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return context


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    """
    Страница редактирования профиля пользователя.
    """
    model = User
    template_name = 'blog/user.html'
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class CreatePost(LoginRequiredMixin, CreateView):
    """
    Страница создания поста.
    """
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    login_url = 'auth/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_date = form.cleaned_data['pub_date']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user}
        )


class AddComment(CreateView):
    """
    Добавление комментария.
    """
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    login_url = '/auth/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id'], })


class EditComment(LoginRequiredMixin, UpdateView):
    """
    Форма редактирования комментария.
    """
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if comment.author != self.request.user:
            return Http404
        return comment

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id'], })


class DeleteComment(LoginRequiredMixin, DeleteView):
    """
    Форма удаления комментария.
    """
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if comment.author != self.request.user:
            return Http404
        return comment

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})
