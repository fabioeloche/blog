"""
Admin configuration for the about application.
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import About


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """
    Admin configuration for About model with Summernote integration.
    """
    list_display = ('title', 'updated_on')
    search_fields = ('title', 'content')
    summernote_fields = ('content',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title',)
        }),
        ('Content', {
            'fields': ('content', 'image'),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('updated_on',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('updated_on',)

    def has_add_permission(self, request):
        """Only allow one About instance."""
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
