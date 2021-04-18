from Portal.models import Document
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models
# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ("content", "title", "reference")
		widgets = {
			'reference': forms.Textarea(attrs={'rows':2, 'cols':15}),
		}


