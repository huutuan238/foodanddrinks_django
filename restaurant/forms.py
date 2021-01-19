from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User, Customer, Comment, Review
from django import forms
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('email','first_name','last_name','username')


class UserUpdateForm(forms.ModelForm):

  class Meta:
    model = User
    fields = ['username', 'first_name','last_name','email']
    widgets = {
      'username': forms.TextInput(attrs={'class':'form-control'}),
      'first_name': forms.TextInput(attrs={'class':'form-control'}),
      'last_name': forms.TextInput(attrs={'class':'form-control'}),
      'email': forms.EmailInput(attrs={'class':'form-control'}),
    }

    help_texts = {
      'username': None,
    }

class PictureWidget(forms.widgets.FileInput):
  def render(self, name, value, attrs=None, **kwargs):
    input_html = super().render(name, value, attrs={"id": "id_avatar"}, **kwargs)
    img_html = mark_safe(f'<br><br><img src="{value.url}" width="150px" height="150px" id="image" />')
    return f'{img_html}{input_html}'


class CustomerUpdateForm(forms.ModelForm):
  avatar = forms.ImageField(widget=PictureWidget)

  class Meta:
    model = Customer
    fields = ['avatar', 'address', 'phone_number']
    widgets = {
      'address': forms.TextInput(attrs={'class':'form-control'}),
      'phone_number': forms.TextInput(attrs={'class':'form-control'}),
    }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReviewForm(forms.ModelForm):
  """docstring for ReviewForm"""
  class Meta:
    model = Review
    fields = ['content', 'vote']
