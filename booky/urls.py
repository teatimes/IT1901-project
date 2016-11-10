from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views

from booky.forms import LoginForm
from booky.views import *

"""Redirects to corresponding Views based on URL regex inside this list"""
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^offer/add/$', OfferCreate.as_view(), name='offer-add'),
    url(r'^offer/(?P<pk>[0-9]+)/$', OfferDetail.as_view(), name='offer-detail'),
    url(r'^offer/(?P<pk>[0-9]+)/edit/$', OfferUpdate.as_view(), name='offer-update'),
    url(r'^offers/$', OfferList.as_view(), name='offer-list'),

    url(r'^artist/add/$', ArtistCreate.as_view(), name='artist-add'),
    url(r'^artist/(?P<pk>[0-9]+)/$', ArtistDetail.as_view(), name='artist-detail'),
    url(r'^artists/', ArtistList.as_view(), name='artist-list'),

    url(r'^event/(?P<pk>[0-9]+)/$', EventDetail.as_view(), name='event-detail'),
    url(r'^events/', EventList.as_view(), name='event-list'),

    url(r'^results/', ResultList.as_view(), name='results'),

    url(r'^login/', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/', views.logout, {'next_page': '/login'}),

    url(r'^calendar/', CalendarView.as_view(), name='calendar'),

    url(r'^admin/', admin.site.urls)
]