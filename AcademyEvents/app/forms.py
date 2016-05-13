"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class TrustSelector(forms.Form):
    trust_name = forms.CharField(required=False)
    trust_number = forms.ChoiceField(required=False, choices=[(x, x) for x in range(6625091, 6625095)])

class SchoolSelector(forms.Form):
    school_name = forms.CharField(required=False)
    school_urn = forms.ChoiceField(required=False, choices=[(x, x) for x in range(137134, 137139)])
    #school_upin = forms.IntegerField(required=False)