"""
Admin configuration for the blog application.
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_on', 'post_count')
    list_filter = ('created_on',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_on', 'post_count')
    list_filter = ('created_on',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for Post model with Summernote integration.
    """
    list_display = ('title', 'author', 'category',
                    'created_on', 'status', 'get_comment_count')
    list_filter = ('created_on', 'category', 'tags', 'author')
    search_fields = ('title', 'content', 'excerpt', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_on'
    summernote_fields = ('content',)
    readonly_fields = ('created_on',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'image'),
            'classes': ('wide',)
        }),
        ('Categorization', {
            'fields': ('category', 'tags'),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('created_on',),
            'classes': ('collapse',)
        }),
    )

    def status(self, obj):
        return 'Published' if obj.created_on else 'Draft'
    status.short_description = 'Status'

    def get_comment_count(self, obj):
        """Return the number of comments for this post."""
        return obj.comments.count()
    get_comment_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    """
    list_display = ('user', 'post', 'content_preview',
                    'created_on', 'approved')
    list_filter = ('approved', 'created_on', 'post')
    search_fields = ('user__username', 'post__title', 'content')
    actions = ['approve_comments', 'disapprove_comments']
    readonly_fields = ('created_on',)

    def content_preview(self, obj):
        """Return a preview of the comment content."""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

    def approve_comments(self, request, queryset):
        """Approve selected comments."""
        updated = queryset.update(approved=True)
        self.message_user(
            request, f'{updated} comments were successfully approved.')
    approve_comments.short_description = 'Approve selected comments'

    def disapprove_comments(self, request, queryset):
        """Disapprove selected comments."""
        updated = queryset.update(approved=False)
        self.message_user(
            request, f'{updated} comments were successfully disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'
