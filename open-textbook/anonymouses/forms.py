from django import forms
from .models import Anonymous, Comment

class AnonymousForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder': '제목을 입력해주세요',

            }
        ),
    )

    class Meta:
        model = Anonymous
        fields = ('title', 'content',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }
        ),
    )
    class Meta:
        model = Comment
        fields = ('content',)