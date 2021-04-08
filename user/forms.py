from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, PostToUser, CommentToPost
from django.db import models

#create your form here !
class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None


	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
		help_texts = {
			'username': None,
			'password': None,
			'email': None,

		} 

	# check unique email 
	def cleaned_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			raise forms.ValidationError("This email already used")
		return data

class ReplyForm(forms.ModelForm):
	class Meta:
		model = CommentToPost
		fields = ['content']