from django import forms
from .models import Anonymous, Comment

class AnonymousForm(forms.ModelForm):
    
    class Meta:
        model = Anonymous
        fields = ('title', 'content',)


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content',)