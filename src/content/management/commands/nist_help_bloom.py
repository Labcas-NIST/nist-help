# encoding: utf-8

'''📐💁 NIST Help: initial content blooming.'''

# from robots.models import Rule, DisallowedUrl

from content.models import HomePage
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from theme.models import Footer
from wagtail.images.models import Image
from wagtail.models import Site, Page
from wagtail.rich_text import RichText
from wagtailmenus.models import FlatMenu, FlatMenuItem
import pkg_resources


class Command(BaseCommand):
    '''Bloom the NIST Help site with initial content and settings.'''

    help = 'Bloom the NIST Help site with initial content and settings'
    search_description = 'NIST LabCAS provides help in its use'

    def get_html_text(self, name: str) -> RichText:
        return RichText(pkg_resources.resource_string(__name__, f'data/{name}.html').decode('utf-8').strip())

    def set_site(self):
        '''Set up the Site object for NIST Help, returning it.'''
        site = Site.objects.filter(is_default_site=True).first()
        site.site_name = 'NIST Help'
        site.hostname = 'labcas.jpl.nasa.gov'
        site.save()
        old_root = site.root_page.specific
        if old_root.title == 'NIST Help':
            return site

        with pkg_resources.resource_stream(__name__, 'data/home-banner.jpg') as f:
            banner_image = ImageFile(f, name='nist-help-banner-image')
            image = Image(title='NIST Help Banner Image', file=banner_image)
            image.save()
            mega_root = old_root.get_parent()
            home_page = HomePage(
                title='NIST Help', seo_title='NIST Help at the Jet Propulsion Laboratory',
                search_description=self.search_description, banner=image, live=True, slug=old_root.slug,
                depth=old_root.depth, url_path=old_root.url_path, path=old_root.path
            )
            home_page.body.append(('rich_text', self.get_html_text('home')))
            site.root_page = home_page
            old_root.delete()
            mega_root.save()
            home_page.save()
            site.save()
            return site

    def set_initial_settings(self, site):
        footer = Footer.objects.get_or_create(site_id=site.id)[0]
        footer.site_manager = 'Ben Smith'
        footer.webmaster = 'David Liu'
        footer.clearance = 'CL № 23-0975'
        footer.save()

    def create_footer_menus(self, site):
        FlatMenu.objects.all().delete()

        # For some reason (possibly because contact-us is a form, not a page), the contact us never gets
        # rendered. So I'm rendering it manually in footer.html.
        #
        # Leaving this code in here in case we want to revisit it:
        #
        # contact = FlatMenu(site=site, title='1: Contact', handle='footer-contact', heading='Contact')
        # contact.save()
        # contact_page = Page.objects.filter(slug='contact-us').first()
        # FlatMenuItem(menu=contact, link_page=contact_page, link_text='Contact Us').save()
        # FlatMenuItem(
        #     menu=contact, link_url='https://www.jpl.nasa.gov/who-we-are/media-information/jpl-media-contacts',
        #     link_text='JPL Media Contacts'
        # ).save()

        social = FlatMenu(site=site, title='4: Social Media', handle='footer-social', heading='Social Media')
        social.save()
        for url, text in (
            ('https://www.facebook.com/NASAJPL', 'Facebook'),
            ('https://twitter.com/NASAJPL', 'Twitter'),
            ('https://www.youtube.com/user/JPLnews', 'YouTube'),
            ('https://www.instagram.com/nasajpl/', 'Instagram')
        ):
            FlatMenuItem(menu=social, link_url=url, link_text=text).save()

    def handle(self, *args, **options):
        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False
            site = self.set_site()
            root = site.root_page
            root.get_children().delete()
            root.refresh_from_db()
            self.set_initial_settings(site)
            self.create_footer_menus(site)
        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = True
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
