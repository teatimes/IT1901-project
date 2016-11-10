from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.base import TemplateView

from booky.common import BaseMixin, has_group, get_artist_user
from booky.models import Event
from .artist_views import ArtistDetail



class HomeView(BaseMixin, TemplateView):
    """
        HomeView called with url '/':

    dispatch:
    ---------
        Redirect based on user affiliations:
            (Role -> View )
            artist -> ArtistDetail(artist)
            admin -> Admin
            manager -> CalendarView


    get_context_data:
    ------------------
        Sends Custom context based on affiliation:
            technician: Events user is assigned to.
            director: Offers that hs is supposed to handle

    """
    template_name = "home.html"

    # Redirection Artist to their Detail page, Admins to AdminView, and restpast
    def dispatch(self, request, *args, **kwargs):
        # Getting ArtistUser Object to be manipulated later on instead of calling it more than once.
        artist = get_artist_user(self.request.user)
        if artist:
            return ArtistDetail.as_view()(request, pk=artist.artist.id)
        elif request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        elif has_group(request.user, 'manager'):
            return HttpResponseRedirect('/calendar/')
        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if has_group(self.request.user, 'technician'):
            context['working_events'] = self.request.user.events_assigned.filter(status=4)
        elif has_group(self.request.user, 'director'):
            context['pending'] = Event.objects.filter(status=0, date__gt=timezone.now())
            context['sent'] = Event.objects.filter(status=2, date__gt=timezone.now())
            context['accepted'] = Event.objects.filter(status=3, date__gt=timezone.now())

        return context
