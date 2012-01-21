from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import redirect_to
from django.conf import settings
from django.http import HttpResponse
import base64
import re


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    # (r'^dashboard/', include('dashboard.foo.urls')),
                       (r'^privacy/', include('privacy.urls')),
                       (r'.*/__history__.html$', lambda r: HttpResponse()),
                       (r'^builds/',
                        include('tinder.urls')),
                       (r'^source/(?P<repo_name>.+)?$',
                        'pushes.views.pushlog', {}, 'pushlog'),
                       (r'^pushes/(?P<remainder>.+)?$', 
                            redirect_to, {'url': '/source/%(remainder)s'}),
                       (r'^dashboard/', include('l10nstats.urls')),
                       (r'^shipping',
                            include('shipping.urls')),
                       (r'^bugs/',
                            include('bugsy.urls')),
                       (r'^webby/',
                            include('webby.urls')),
                       (r'^accounts/',
                            include('accounts.urls')),
                       (r'^',
                        include('homepage.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# Usually, you would include this only for DEBUG, but let's keep
# this so that we can reverse resolve static.
# That way, we can move the site to /stage/foo without messing with
# the references to /media/.

# Remove leading and trailing slashes so the regex matches.
# TODO: consider subclassing django.views.static.serve with something
# that prints a warning message
static_url = settings.STATIC_URL.lstrip('/').rstrip('/')
urlpatterns += patterns('',
    url(r'^%s/(?P<path>.*)$' % static_url, 'django.views.static.serve',
     {'document_root': settings.STATIC_ROOT},
     'static'),
)

#if settings.DEBUG:
urlpatterns += staticfiles_urlpatterns()

# Proxy the webdashboard
urlpatterns += patterns('',
                        (r'^webdashboard/(?P<path>.*)$',
                         'l10nstats.views.proxy',
                         {'base': 'http://l10n.mozilla.org/webdashboard/'}, 'webdashboard'),
                        )
