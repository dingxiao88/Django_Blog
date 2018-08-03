from django import forms
from .models import Comment
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):

    captcha = CaptchaField(label='验证码')

    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']