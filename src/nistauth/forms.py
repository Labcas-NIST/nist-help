# encoding: utf-8

from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django_auth_ldap.backend import LDAPBackend


class BootstrapErrorList(ErrorList):
    '''Custom ErrorList that uses a Bootstrap-compatible default CSS class.'''
    def __init__(self, initlist=None, error_class=None, renderer=None):
        if error_class is None:
            error_class = 'text-danger'
        super().__init__(initlist, error_class, renderer)


class PasswordResetForm(forms.Form):
    # Renering
    error_css_class = 'is-invalid'
    required_css_class = 'is-required'
    error_class = BootstrapErrorList
    template_name = 'nistauth/form-rendering.html'
    template_name_label = 'nistauth/label-rendering.html'

    # Fields
    username = forms.CharField(max_length=32)
    current_password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='New password', max_length=128, widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='New password, again', max_length=128, widget=forms.PasswordInput())

    # Validation
    def clean(self):
        cleaned_data = super().clean()
        new_password1, new_password2 = cleaned_data.get('new_password1'), cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            errors = {
                'new_password1': "This password didn't match the second password",
                'new_password2': "This password didn't match the first password"
            }
            raise ValidationError(errors, code='invalid')

        # TODO: password complexity?
        
        current = cleaned_data.get('current_password')
        if current == new_password1:
            errors = {
                'current_password': 'The current password must be different from the new password',
                'new_password1': 'The new password must be different from the current password',
                'new_password2': 'The new password must be different from the current password',
            }
            raise ValidationError(errors, code='invalid')
        username = cleaned_data.get('username')
        backend = LDAPBackend()
        if not backend.authenticate(request=None, username=username, password=current):
            errors = {
                'current_password': f"The password for «{username}» isn't correct or «{username}» is an unknown user"
            }
            raise ValidationError(errors, code='invalid')
