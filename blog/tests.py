"""
Tests for the blog application.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm


class PostModelTest(TestCase):
    """Test cases for Post model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post content.',
            excerpt='Test excerpt'
        )

    def test_post_creation(self):
        """Test post creation."""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.slug, 'test-post')

    def test_post_str_representation(self):
        """Test string representation of post."""
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_get_absolute_url(self):
        """Test get_absolute_url method."""
        expected_url = reverse('blog:post_detail', kwargs={
                               'slug': 'test-post'})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_post_get_excerpt(self):
        """Test get_excerpt method."""
        self.assertEqual(self.post.get_excerpt(), 'Test excerpt')

        # Test with long content
        long_post = Post.objects.create(
            title='Long Post',
            slug='long-post',
            author=self.user,
            content='This is a very long post content that should be truncated when no excerpt is provided. ' * 10
        )
        excerpt = long_post.get_excerpt()
        self.assertTrue(len(excerpt) <= 203)  # 200 chars + '...'
        self.assertTrue(excerpt.endswith('...'))

    def test_post_approved_comments(self):
        """Test approved_comments method."""
        approved_comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Approved comment',
            approved=True
        )
        unapproved_comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Unapproved comment',
            approved=False
        )

        approved_comments = self.post.approved_comments()
        self.assertIn(approved_comment, approved_comments)
        self.assertNotIn(unapproved_comment, approved_comments)


class CommentModelTest(TestCase):
    """Test cases for Comment model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Test comment content'
        )

    def test_comment_creation(self):
        """Test comment creation."""
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, 'Test comment content')
        self.assertFalse(self.comment.approved)

    def test_comment_str_representation(self):
        """Test string representation of comment."""
        expected = f'Comment by {self.user.username} on {self.post.title}'
        self.assertEqual(str(self.comment), expected)

    def test_comment_get_absolute_url(self):
        """Test get_absolute_url method."""
        expected_url = reverse('blog:post_detail', kwargs={
                               'slug': 'test-post'})
        self.assertEqual(self.comment.get_absolute_url(), expected_url)


class CommentFormTest(TestCase):
    """Test cases for CommentForm."""

    def test_valid_comment_form(self):
        """Test valid comment form."""
        form_data = {
            'content': 'This is a valid comment with more than 10 characters.'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form_too_short(self):
        """Test comment form with too short content."""
        form_data = {
            'content': 'Short'
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('at least 10 characters', str(form.errors))

    def test_invalid_comment_form_too_long(self):
        """Test comment form with too long content."""
        form_data = {
            'content': 'A' * 1001
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cannot exceed 1000 characters', str(form.errors))

    def test_comment_form_clean_content(self):
        """Test content cleaning."""
        form_data = {
            'content': '  This comment has extra spaces  '
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data['content'], 'This comment has extra spaces')


class BlogViewsTest(TestCase):
    """Test cases for blog views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content'
        )

    def test_post_list_view(self):
        """Test post list view."""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Test Post')

    def test_post_list_view_with_search(self):
        """Test post list view with search."""
        response = self.client.get(
            reverse('blog:post_list'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

        response = self.client.get(reverse('blog:post_list'), {
                                   'search': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Post')

    def test_post_detail_view(self):
        """Test post detail view."""
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Test Post')

    def test_post_detail_view_invalid_slug(self):
        """Test post detail view with invalid slug."""
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': 'invalid-slug'}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_with_comment_submission(self):
        """Test comment submission on post detail view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('blog:post_detail', kwargs={'slug': 'test-post'}),
            {'content': 'This is a test comment with enough characters.'}
        )
        # Redirect after successful submission
        self.assertEqual(response.status_code, 302)

        # Check if comment was created
        comment = Comment.objects.first()
        self.assertEqual(
            comment.content, 'This is a test comment with enough characters.')
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user)
        self.assertFalse(comment.approved)

    def test_comment_edit_view_authenticated(self):
        """Test comment edit view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Original comment'
        )

        response = self.client.get(
            reverse('blog:comment_edit', kwargs={'comment_id': comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_edit.html')

    def test_comment_edit_view_unauthenticated(self):
        """Test comment edit view for unauthenticated user."""
        comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Original comment'
        )

        response = self.client.get(
            reverse('blog:comment_edit', kwargs={'comment_id': comment.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_comment_edit_view_wrong_user(self):
        """Test comment edit view for wrong user."""
        self.client.login(username='testuser', password='testpass123')

        comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Original comment'
        )

        response = self.client.get(
            reverse('blog:comment_edit', kwargs={'comment_id': comment.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to post detail

    def test_comment_delete_view_authenticated(self):
        """Test comment delete view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Comment to delete'
        )

        response = self.client.get(
            reverse('blog:comment_delete', kwargs={'comment_id': comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_delete.html')

    def test_comment_delete_view_unauthenticated(self):
        """Test comment delete view for unauthenticated user."""
        comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Comment to delete'
        )

        response = self.client.get(
            reverse('blog:comment_delete', kwargs={'comment_id': comment.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_comment_delete_ajax_view(self):
        """Test AJAX comment delete view."""
        self.client.login(username='testuser', password='testpass123')
        comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Comment to delete'
        )

        response = self.client.post(
            reverse('blog:comment_delete_ajax',
                    kwargs={'comment_id': comment.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

        # Check if comment was deleted
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())


class AboutViewsTest(TestCase):
    """Test cases for about views."""

    def test_about_view(self):
        """Test about view."""
        from about.models import About

        # Test without about content
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')

        # Test with about content
        About.objects.create(
            title='About Us',
            content='This is about us content.'
        )

        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us')
        self.assertContains(response, 'This is about us content.')
