"""
Views for the about application.
"""
from django.shortcuts import render
from .models import About


def about_view(request):
    """
    Display the About page.

    Args:
        request: HTTP request object

    Returns:
        Rendered template with About page content
    """
    try:
        about = About.objects.first()
    except About.DoesNotExist:
        about = None

    context = {
        'about': about,
    }
    return render(request, 'about/about.html', context)
