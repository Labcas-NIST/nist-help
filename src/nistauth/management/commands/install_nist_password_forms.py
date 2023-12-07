# encoding: utf-8

from django.conf import settings
from django.core.management.base import BaseCommand
from nistauth.models import PasswordResetPage
from wagtail.models import Site
from wagtail.rich_text import RichText


class Command(BaseCommand):
    help = 'Install NIST password management forms'

    def _install_password_forms(self):
        site = Site.objects.filter(is_default_site=True).first()
        home = site.root_page
        PasswordResetPage.objects.descendant_of(home).delete()
        preamble = RichText('''<p class='small'>Don't know your username or current password?
            <a href='mailto:nist-labcas@jpl.nasa.gov'>Email us</a> and we'll help you out.</p>
        ''')
        prp = PasswordResetPage(title='Password Reset', show_in_menus=True, preamble=preamble)
        home.add_child(instance=prp)
        prp.save()

    def handle(self, *args, **options):
        self.stdout.write('Installing NIST password forms')

        old = getattr(settings, 'WAGTAILREDIRECTS_AUTO_CREATE', True)
        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False
            self._install_password_forms()
        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = old
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
            self.stdout.write("Job's done!")
