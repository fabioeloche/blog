"""
Views for the blog application.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment, Category, Tag
from .forms import CommentForm


def post_list(request):
    """
    Display a paginated list of all blog posts.

    Args:
        request: HTTP request object

    Returns:
        Rendered template with paginated posts
    """
    posts = Post.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """
    Display a single blog post with its comments and related posts.

    Args:
        request: HTTP request object
        slug: URL slug of the post

    Returns:
        Rendered template with post details, comments, and related posts
    """
    post = get_object_or_404(Post, slug=slug)
    comments = post.approved_comments()
    comment_form = CommentForm()
    related_posts = post.get_related_posts(limit=3)

    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(
                request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('blog:post_detail', slug=slug)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """
    Display posts filtered by category.

    Args:
        request: HTTP request object
        slug: Category slug

    Returns:
        Rendered template with category posts
    """
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)

    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """
    Display posts filtered by tag.

    Args:
        request: HTTP request object
        slug: Tag slug

    Returns:
        Rendered template with tag posts
    """
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)

    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_posts.html', context)


@login_required
def comment_edit(request, comment_id):
    """
    Edit a user's own comment.

    Args:
        request: HTTP request object
        comment_id: ID of the comment to edit

    Returns:
        Rendered template or redirect
    """
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if user owns the comment
    if comment.user != request.user:
        messages.error(request, 'You can only edit your own comments.')
        return redirect('blog:post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = False  # Reset approval status
            comment.save()
            messages.success(
                request, 'Your comment has been updated and is awaiting approval.')
            return redirect('blog:post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'comment': comment,
        'post': comment.post,
    }
    return render(request, 'blog/comment_edit.html', context)


@login_required
def comment_delete(request, comment_id):
    """
    Delete a user's own comment.

    Args:
        request: HTTP request object
        comment_id: ID of the comment to delete

    Returns:
        JSON response or redirect
    """
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if user owns the comment
    if comment.user != request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'You can only delete your own comments.'})
        messages.error(request, 'You can only delete your own comments.')
        return redirect('blog:post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, 'Your comment has been deleted.')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Comment deleted successfully.'})

        return redirect('blog:post_detail', slug=post_slug)

    context = {
        'comment': comment,
        'post': comment.post,
    }
    return render(request, 'blog/comment_delete.html', context)


@require_POST
@login_required
def comment_delete_ajax(request, comment_id):
    """
    AJAX endpoint for deleting comments.

    Args:
        request: HTTP request object
        comment_id: ID of the comment to delete

    Returns:
        JSON response
    """
    try:
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if user owns the comment
        if comment.user != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You can only delete your own comments.'
            })

        comment.delete()
        return JsonResponse({
            'success': True,
            'message': 'Comment deleted successfully.'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error deleting comment: {str(e)}'
        })
