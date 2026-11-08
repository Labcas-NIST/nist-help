# encoding: utf-8

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Upgrade NIST Help portal to the latest version'

    def upgrade_nist_help(self):
        self.stdout.write('(Currently does nothing.)')

    def handle(self, *args, **options):
        self.stdout.write('Upgrading NIST Help portal to the latest version')

        old = getattr(settings, 'WAGTAILREDIRECTS_AUTO_CREATE', True)
        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False
            self.upgrade_nist_help()
        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = old
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
            self.stdout.write("Job's done!")
