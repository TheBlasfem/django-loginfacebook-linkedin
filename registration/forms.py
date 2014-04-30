# coding=utf-8
__author__ = 'martin'
import re

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext as _

from hackusername.models import MyUser

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': _(u'Password')}), required=True)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': _(u'Password confirmation')}), required=True)

    class Meta:
        model = MyUser
        fields = ('name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _(u'name')}),
            'email': forms.EmailInput(attrs={'placeholder': _(u'Enter your email')}),
        }
        labels = {
            'email': '',
            'name': '',
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        r = re.compile("(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])")
        if r.search(password1) is None:
            raise forms.ValidationError(_(u"Enter at least one digit and one capital"))
        if len(password1) < 8:
            raise forms.ValidationError(_(u"Enter at 8 characters"))
        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_(u"Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    #password = ReadOnlyPasswordHashField()

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput, required=False)

    class Meta:
        model = MyUser
        fields = ('email', 'date_of_birth', #'password', 'is_active', 'is_admin',
                  'password1',
                  'password2',
                  'name',
                  'commercial_name',
                  'business_name',
                  'ruc',
                  'address',
                  'phone',
                  'web',
                  'description'
                  )
        """labels = {
            'email': '',#_(u'Enter your email'),
            'date_of_birth': '',#_(u'Date of birth'),
            'name': '',#_(u'Name'),
            'commercial_name': '',#_(u'Commercial Name'),
            'business_name': '',#_(u'Business Name'),
            'address': '',#_(u'Address'),
            'phone': '',#_(u'Phone'),
            'description': '',#_(u'Description')
        }"""
        labels = {
            'email': _(u'Enter your email'),
            'date_of_birth': _(u'Date of birth'),
            'name': _(u'Name'),
            'commercial_name': _(u'Commercial Name'),
            'business_name': _(u'Business Name'),
            'address': _(u'Address'),
            'phone': _(u'Phone'),
            'description': _(u'Description')
        }
        help_texts = {}
        error_messages = {
            'email': {
                'required': _(u'You have to enter your email.'),
                'invalid': _(u'Please enter a valid email'),
                '': _
            },
            'web': {
                'invalid': _(u'Please enter a valid url'),
            },
            'date_of_birth': {
                'invalid': _(u'Please enter a valid date YYYY/MM/DD'),
            },
        }

        """widgets = {
            'commercial_name': forms.TextInput(attrs={'placeholder': 'aaa'}),
        }"""

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserChangeForm, self).save(commit=False)

        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=255, label='', widget=forms.EmailInput(attrs={'placeholder': _(u'Enter your email')}), required=True)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': _('Password')}), required=True)