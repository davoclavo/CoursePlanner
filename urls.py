from django.conf.urls.defaults import *
from CoursePlanner.views import * 
from django.contrib import admin 
import os.path


admin.autodiscover()

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns('',
    (r'^$', home),
    (r'^CoursePlanner/$', main),
    (r'^logout/$', logout_page),
    (r'^all/$', all),
    (r'^sms/$', sms),
    (r'^admin/', include(admin.site.urls)),
    
    # Site Media
    (r'site_media/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': site_media }),
)
