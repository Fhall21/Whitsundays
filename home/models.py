import json, random

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404



from wagtail.contrib.forms.models import AbstractForm, AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, PageBase
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         StreamFieldPanel)

from home.blocks import VideoIdsBlock
from modelcluster.fields import ParentalKey


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None


    '''
    name = models.CharField(max_length=250, null=True, blank=False)
    email = models.EmailField(max_length=250, null=True, blank=False)

    def __str__(self):
        return self.name
'''
class Video(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=False, null=True)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="") 

    def __str__(self):
        return self.name

class VideoSubmission(Page):
    headline = models.CharField(max_length=200, null=True, blank=True)
    intro_video_id = models.CharField(max_length=50, null=True, blank=True)
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video_ids = StreamField([('video_ids', VideoIdsBlock())], null=True, blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('headline'),
        FieldPanel('intro_video_id'),
        ImageChooserPanel('background_image'),
        StreamFieldPanel('video_ids'),

    ] 

    def serve(self, request):

        if request.method == 'GET':
            #retreiving user from session variables
            new_user_username = request.session.get('new_user_username', None)
            try:
                new_user = User.objects.get(username=new_user_username)
                arg = {
                'new_user':new_user,
                'page': self,
                }
            except User.DoesNotExist:
                arg = {'page': self}
            request.session['new_user'] = None
            return render(request, 'home/video_submission.html', arg)
class HomePage(Page):
    headline = models.CharField(max_length=200, null=True, blank=True)
    intro_video_id = models.CharField(max_length=50, null=True, blank=True)
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    thank_you_page_title = models.CharField(max_length=200, null=True, blank=True)

    thank_you_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('headline'),
        FieldPanel('intro_video_id'),
        ImageChooserPanel('background_image'),
        FieldPanel('thank_you_text'),
        FieldPanel('thank_you_page_title'),

    ] 

    def serve(self, request):
        from home.forms import UserCreateForm

        if request.method == 'POST':
            form = UserCreateForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                _username = '{}_{}'.format(form.cleaned_data['first_name'], form.cleaned_data['last_name'])

                #creating uniqe username
                unique = False
                while not(unique):
                    if User.objects.filter(username=_username).exists():
                        _username += '{}'.format(random.randint(0,999))
                    else:
                        #if it's unique then create user
                        unique = True
                        p, created = User.objects.get_or_create(
                            username = _username,
                            email = email,
                            defaults={
                            'first_name':form.cleaned_data['first_name'],
                            'last_name':form.cleaned_data['last_name']
                            })

                print (p)
                #getting the redirect link if there is one
                home_page_obj = HomePage.objects.first()
                video_submission_page = VideoSubmission.objects.descendant_of(home_page_obj).first()
                if video_submission_page:
                    direct_url = '/{}/'.format(str(video_submission_page).replace(' ', '-')).lower() # adding / and replacing spacing with - while making it all lowercase

                    #adding new user as a session variable to be accessed later
                    request.session['new_user_username'] = p.username
                    #redirecting to video submition page
                    return redirect(direct_url)


                return render(request, 'home/video_submission.html', {
                                    'page': self,
                                    'user':p,})
        else:
            form = UserCreateForm()
        return render(request, 'home/home_page.html', {
            'page': self,
            'form': form
            })


    #if user has already exists
    '''
    #serve is like the basic view in views.py
    def serve(self, request, *args, **kwargs):
        if self.get_submission_class().objects.filter(page=self, 
            email=request.user.pk).exists():
                return render(
                    request,
                    self.template,
                    self.get_context(request)
                    )
    '''



    #using own submission class
    def get_submission_class(self):
        return CustomFormSubmission

    def process_form_submission(self, form):
        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self, email=form.cleaned_data['email']
            )

#own class
class CustomFormSubmission(AbstractFormSubmission):
    email = models.EmailField(max_length=100, blank=False)

'''
to use with previous to stop multiple same emails being used
    class Meta:
        unique_together = ('page', 'email')
'''