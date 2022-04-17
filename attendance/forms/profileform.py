from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError

ACTIVE_CHOICES=[
    ('1', 'Yes'),
    ('0', 'No')
]

USER_TYPES=[
    ('facilitator', 'Facilitator'),
    ('mentor', 'Mentor')
]

class ProfileForm(forms.Form):
    _user = False

    user_id = forms.CharField(label="UserID", widget=forms.HiddenInput())
    username = forms.CharField(label='Username', max_length=100, help_text="Required.")
    first = forms.CharField(label='First Name', max_length=100)
    last = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label="Email address", required=True, help_text="Required.")
    useractive = forms.ChoiceField(label='Active', required=True, choices=ACTIVE_CHOICES)
    usertype = forms.ChoiceField(label='Type', choices=USER_TYPES)
    newpassword = forms.CharField(label='Password', max_length=100, required=False, widget=forms.PasswordInput, help_text="Leave blank to retain existing password.")
    repeatpassword = forms.CharField(label='Repeat Password', max_length=100, required=False, widget=forms.PasswordInput)

    def _getUser(self):
        if self._user:
            return self._user
        if self.cleaned_data['user_id'] != 'NEW':
            self._user = User.objects.get(id=self.cleaned_data['user_id'])
            if not self._user:
                raise ValidationError("Invalid User ID.")
            return self._user

    def clean_username(self):
        un = self.cleaned_data['username']
        if self.cleaned_data['user_id'] == 'NEW':
            if User.objects.filter(username=un).exists():
                raise ValidationError("That username already exists.")
        else:
            user = self._getUser()
            if user.username != un:
                if User.objects.filter(username=un).exists():
                    raise ValidationError("That username already exists.")


    def clean_email(self):
        email = self.cleaned_data['email']
        if self.cleaned_data['user_id'] == 'NEW':
            if User.objects.filter(email=email).exists():
                raise ValidationError("That email already exists.")
        else:
            user = self._getUser()
            if user.email != email:
                if User.objects.filter(email=email).exists():
                    raise ValidationError("That email already exists.")

    def clean(self):
        p1 = self.cleaned_data['newpassword']
        if self.cleaned_data['user_id'] == 'NEW':
            validate_password(p1)
            p2 = self.cleaned_data['repeatpassword']
            if p1 != p2:
                raise ValidationError("Passwords must match.")
        else:
            if p1 != '':
                validate_password(p1)
                p2 = self.cleaned_data['repeatpassword']
                if p1 != p2:
                    raise ValidationError("Passwords must match.")



