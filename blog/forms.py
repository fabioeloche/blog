"""
Forms for the blog application.
"""
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments.

    Attributes:
        content: Text area for comment content with custom styling
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Share your thoughts...',
            'style': 'resize: vertical;'
        }),
        label='Comment',
        help_text='Your comment will be reviewed before being published.'
    )

    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        """Initialize form with custom styling."""
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Share your thoughts...',
            'style': 'resize: vertical;'
        })

    def clean_content(self):
        """Validate comment content."""
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 10:
            raise forms.ValidationError(
                'Comment must be at least 10 characters long.'
            )
        if len(content) > 1000:
            raise forms.ValidationError(
                'Comment cannot exceed 1000 characters.'
            )
        return content.strip()
