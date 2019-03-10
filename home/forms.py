from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


from home.models import Video



class videoUploadForm(forms.ModelForm):

	class Meta:
		model = Video
		fields = ['name', 'video']

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
	    model = User
	    fields = ('first_name','last_name','username','email', 'password1', 'password2')

	    labels = {
	    'last_name': _('Last name (optional)'),
	    }

	def __init__(self, *args, **kwargs):
	    super(UserCreateForm,self).__init__(*args, **kwargs)
	    #remove what you like...
	    #self.fields.pop('first_name')
	    self.fields.pop('username')
	    self.fields.pop('password1')
	    self.fields.pop('password2')

'''
	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		clean_email = self.cleaned_data['email']
		user.email = clean_email
		user.username = self.cleaned_data['username']
		if commit:
			user.save()
		return user
class videoUploaderForm(forms.ModelForm):

	class Meta:
		model = videoUploader
		fields = ['name', 'email']'''