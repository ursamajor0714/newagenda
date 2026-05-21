from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 13:
            raise forms.ValidationError('아이디는 13자리 이하로 입력해주세요.')
        if not username.isalnum():
            raise forms.ValidationError('아이디는 영어 대소문자와 숫자만 가능합니다.')
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
