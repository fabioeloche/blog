"""
Models for the blog application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """
    Model representing a blog post category.

    Attributes:
        name: The name of the category
        slug: URL-friendly version of the name
        description: Optional description of the category
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Tag(models.Model):
    """
    Model representing a blog post tag.

    Attributes:
        name: The name of the tag
        slug: URL-friendly version of the name
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    """
    Model representing a blog post.

    Attributes:
        title: The title of the post
        slug: URL-friendly version of the title
        author: Foreign key to User model
        content: Rich text content of the post
        created_on: Timestamp when post was created
        image: Optional image for the post
        excerpt: Short excerpt from the content
        category: Foreign key to Category model
        tags: Many-to-many relationship with Tag model
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    excerpt = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """String representation of the post."""
        return self.title

    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL to access a particular post."""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_excerpt(self):
        """Return excerpt or first 200 characters of content."""
        if self.excerpt:
            return self.excerpt
        return self.content[:200] + '...' if len(self.content) > 200 else self.content

    def approved_comments(self):
        """Return only approved comments for this post."""
        return self.comments.filter(approved=True)

    def get_related_posts(self, limit=3):
        """
        Get related posts based on category and tags.

        Args:
            limit: Maximum number of related posts to return

        Returns:
            QuerySet of related posts
        """
        related_posts = Post.objects.exclude(id=self.id)

        # First, try to find posts with the same category
        if self.category:
            category_posts = related_posts.filter(category=self.category)
            if category_posts.count() >= limit:
                return category_posts[:limit]

        # Then, try to find posts with similar tags
        if self.tags.exists():
            tag_posts = related_posts.filter(
                tags__in=self.tags.all()).distinct()
            if tag_posts.count() >= limit:
                return tag_posts[:limit]

        # If not enough related posts, get recent posts from the same author
        if related_posts.filter(author=self.author).count() >= limit:
            return related_posts.filter(author=self.author)[:limit]

        # Finally, get recent posts
        return related_posts[:limit]


class Comment(models.Model):
    """
    Model representing a comment on a blog post.

    Attributes:
        post: Foreign key to Post model
        user: Foreign key to User model
        content: Text content of the comment
        created_on: Timestamp when comment was created
        approved: Boolean indicating if comment is approved by admin
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """String representation of the comment."""
        return f'Comment by {self.user.username} on {self.post.title}'

    def get_absolute_url(self):
        """Return the URL to access the post this comment belongs to."""
        return self.post.get_absolute_url()
