from django.conf.urls import patterns, include, url
from django.contrib import admin

from badge_site.views import (
	IndexView, 
	IssuerCreateView, IssuerUpdateView, 
	BadgeCreateView, BadgeUpdateView,
	AwardCreateView, AwardUpdateView
)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),

    
    url(r'^issuer/add/$', IssuerCreateView.as_view(), name='create_issuer'),
    url(r'^issuer/edit/(?P<pk>\d+)/$', IssuerUpdateView.as_view(), name='edit_issuer'),
    url(r'^badge/add/$', BadgeCreateView.as_view(), name='create_badge'),
    url(r'^badge/edit/(?P<pk>\d+)/$', BadgeUpdateView.as_view(), name='edit_issuer'),
    url(r'^award/add/$', AwardCreateView.as_view(), name='create_award'),
    url(r'^award/edit/(?P<pk>\d+)/$', AwardUpdateView.as_view(), name='edit_issuer'),
    

    url(r'^admin/', include(admin.site.urls)),
)
