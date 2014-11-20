from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class NewListForm(forms.Form):
	name = forms.CharField( max_length=50, label='name', required=True, widget=forms.TextInput(attrs={'size': 50}))

	def clean_name(self):
		name = self.cleaned_data['name'].strip()
		if not name:
			raise forms.ValidationError('This field is required.')
		return name

class NewLinkForm(forms.Form):
	name = forms.CharField( required=True, label='name', max_length=50, widget=forms.TextInput(attrs={'size': 50}))
	link = forms.URLField ( required=True, label='link' )
	tags = forms.CharField( required=False, label='tags', widget = forms.Textarea )

	def clean_name(self):
		name = self.cleaned_data['name'].strip()
		if not name:
			raise forms.ValidationError('This field is required.')
		return name

	def clean_link(self):
		link = self.cleaned_data['link'].strip()
		if not link:
			raise forms.ValidationError('This field is required.')
		return link

	def clean_tags(self):
		tags = self.cleaned_data['tags'].strip()
		return tags

class RegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ("username","email", "password")