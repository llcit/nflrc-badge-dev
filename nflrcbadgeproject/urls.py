from django.conf.urls import patterns, include, url
from django.contrib import admin

from badge_site.views import (
	IndexView, BadgeClaimView,
	IssuerCreateView, IssuerUpdateView, IssuerListView,
	BadgeCreateView, BadgeUpdateView, BadgeListView,
	AwardCreateView, AwardUpdateView, AwardListView
)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),

    
    url(r'^issuer/add/$', IssuerCreateView.as_view(), name='create_issuer'),
    url(r'^issuer/edit/(?P<pk>\d+)/$', IssuerUpdateView.as_view(), name='edit_issuer'),
    url(r'^issuers/$', IssuerListView.as_view(), name='list_issuers'),
    
    url(r'^badge/add/(?P<issuer>\d+)/$', BadgeCreateView.as_view(), name='create_badge_by_issuer'),
    url(r'^badge/edit/(?P<pk>\d+)/$', BadgeUpdateView.as_view(), name='edit_badge'),
    url(r'^badges/$', BadgeListView.as_view(), name='list_badges'),
    
    url(r'^award/add/(?P<badge>\d+)/$', AwardCreateView.as_view(), name='create_award_by_badge'),
    url(r'^award/edit/(?P<pk>\d+)/$', AwardUpdateView.as_view(), name='edit_award'),
    url(r'^awards/$', AwardListView.as_view(), name='list_awards'),
    url(r'^awards/(?P<pk>\d+)/$', AwardListView.as_view(), name='list_awards_by_badge'),
    
    url(r'^claim/$', BadgeClaimView.as_view(), name='claim_badge'),
    url(r'^claim/(?P<claim_code>\w+)/$', BadgeClaimView.as_view(), name='claim_badge_with_code'),

    url(r'^admin/', include(admin.site.urls)),
)
