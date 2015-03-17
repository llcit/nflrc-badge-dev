from django.conf.urls import patterns, include, url
from django.contrib import admin

from badge_site.views import IndexView, IssuerCreateView, BadgeCreateView, AwardCreateView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    
    url(r'^issuer/add/$', IssuerCreateView.as_view(), name='create_issuer'),
    url(r'^badge/add/$', BadgeCreateView.as_view(), name='create_badge'),
    url(r'^award/add/$', AwardCreateView.as_view(), name='create_award'),
    

    url(r'^admin/', include(admin.site.urls)),
)
