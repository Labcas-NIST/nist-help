# encoding: utf-8

from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from wagtail.models import Page
from django_auth_ldap.backend import LDAPBackend
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


def _bootstrap(form: forms.Form):
    '''Add Boostrap class to every widget except checkboxes & radio buttons.'''
    for field in form.fields.values():
        if not isinstance(
            field.widget, (
                forms.widgets.CheckboxInput, forms.widgets.CheckboxSelectMultiple, forms.widgets.RadioSelect
            )
        ):
            field.widget.attrs.update({'class': 'form-control'})


class PasswordResetPage(Page):
    page_description = 'A page displaying a form to enable users to reset their passwords'
    preview_modes = []

    preamble = RichTextField(blank=True, help_text='Introductory text to appear above the form')

    content_panels = Page.content_panels + [FieldPanel('preamble')]

    def serve(self, request: HttpRequest) -> HttpResponse:
        from .forms import PasswordResetForm
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                # If all good:
                backend = LDAPBackend()
                username, pwd = form.cleaned_data['username'], form.cleaned_data['current_password']
                newpwd = form.cleaned_data['new_password1']
                user = backend.authenticate(request, username, pwd)
                user.ldap_user.connection.passwd_s(user.ldap_user.dn, pwd, newpwd)
                params = {'page': self, 'username': form.cleaned_data['username']}
                return render(request, 'nistauth/password-changed.html', params)
            # If it's not valid, an exception was raised, so no "else" is needed here
        else:
            # Fresh form
            form = PasswordResetForm()
        _bootstrap(form)
        return render(request, 'nistauth/reset-password.html', {'page': self, 'form': form})
