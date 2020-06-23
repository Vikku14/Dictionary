from django import forms
from .models import Profile, ProfilePhoto
from django.contrib.auth.models import User
from django.core.files import File
from PIL import Image
from django.core.exceptions import ValidationError


def ForbiddennamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup',
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator',
        'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs',
        'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
        'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads',
        'contact', 'blogs', 'feed', 'faq', 'intranet', 'log', 'registration', 'search',
        'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity', 'library']
    if value.lower() in forbidden_usernames:
        raise ValidationError('This Name is not available.')

def InvalidnameValidator(value):
    if '@' in value or '+' in value or '.' in value:
        raise ValidationError('Enter a valid Name.')

def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value, username__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].validators.append(ForbiddennamesValidator)
        self.fields['last_name'].validators.append(ForbiddennamesValidator)
        self.fields['first_name'].validators.append(InvalidnameValidator)
        self.fields['last_name'].validators.append(InvalidnameValidator)

        # self.fields['email'].validators.append(UniqueEmailValidator)


        self.fields['email'].label = "Email"

        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields =('location', 'birth_date', 'bio',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['birth_date'].widget = forms.DateInput()
        self.fields['bio'].widget.attrs['placeholder'] = 'Write something about You.'
        self.fields['location'].widget.attrs['placeholder'] = 'Enter Your Location'
        self.fields['bio'].widget.attrs['rows'] = 4



class ProfilePhotoForm(forms.ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = ProfilePhoto
        fields =( 'photo','x', 'y', 'width', 'height',)

    def save(self):
        picture = super(ProfilePhotoForm, self).save()

        x = self.cleaned_data['x']
        y = self.cleaned_data['y']
        w = self.cleaned_data['width']
        h = self.cleaned_data['height']

        image = Image.open(picture.photo)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((500, 500), Image.ANTIALIAS)
        resized_image.save(picture.photo.path)

        return picture
