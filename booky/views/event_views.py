from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView

from booky.common import BaseMixin, get_artist_user
from booky.forms import EventFilter
from booky.forms import RequirementForm
from booky.models import Event



class EventList(BaseMixin, ListView):
    """
        EventList redirected from url '/events/'

        dispatch:
        ---------
            Checks if user is a artist user:
                if yes, redirect home

        get_queryset:
        -------------
            Is for filter function, handles:
                stage: What stage event is set on
                genre: What the genre of bands that is participating
                semester: What semester the event is booked for

        get_context_data:
        -----------------
            returns extra FilterForm to handle event filters.
    """
    template_name = 'event/event_list.html'

    # Denies permission to artists
    def dispatch(self, request, *args, **kwargs):
        if get_artist_user(request.user):
            return HttpResponseRedirect('/')
        return super(EventList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Event.objects.filter(status=4).order_by('date')

        if get_artist_user(self.request.user):
            queryset = queryset.filter(artist__name=get_artist_user(self.request.user).artist.name)

        # Get stage, genre and semseter
        stage, genre, semester = self.request.GET.get('stage') or 'All', \
                                 self.request.GET.get('genre') or 'All', \
                                 self.request.GET.get('semester') or 'All'

        # Function to create formatted date, e.g. "2016-12-31"
        _d = lambda month, day: '{}-{}-{}'.format(semester[:4], month, day)

        # Filter by semester
        if semester != 'All':
            queryset = queryset.filter(
                date__range=[_d(1, 1), _d(6, 30)] if semester[-1] == 'v' else [_d(7, 1), _d(12, 31)])

        # Filter by stage
        if stage != 'All':
            queryset = queryset.filter(stage__name=stage)

        # Filter by genre
        if genre != 'All':
            queryset = queryset.filter(artist__genre__name=genre)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        # todo trenger vi dette?
        # context['genres'] = Genre.objects.all()
        # context['stages'] = Stage.objects.all()
        context['event_form'] = EventFilter(self.request.GET or None)
        return context





class EventDetail(BaseMixin, DetailView):
    """
        EventDetail redirected from url '/event/:pk'

        dispatch:
        ---------
        Checks if user is a artist user not connected to event.artist:
            if false, redirect home

        get_queryset:
        -------------
        Get all Events that has status 'Published"

        post:
        ------
        handles POST request set towards event.requirements

        get_context_data:
        -----------------
        returns RequirementsForm, and two lists 'rigging' and 'sound_light'
        that contains technicians that is going to work this event
    """
    template_name = 'event/event_detail.html'

    def dispatch(self, request, *args, **kwargs):
        artist_user = get_artist_user(request.user)
        # Checks if first part of 'and' is true, ignores part two if false, that's why it works
        if artist_user and artist_user.artist.id != self.get_object().artist.id:
            return HttpResponseRedirect('/events/')
        return super(EventDetail, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Event.objects.filter(status=4)

    def post(self, request, *args, **kwargs):
        form = RequirementForm(request.POST, instance=self.get_object())
        form.save()
        return super(EventDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['req_form'] = RequirementForm(instance=self.get_object())
        context['rigging'] = Event.objects.get(pk=self.get_object().pk).technicians.filter(groups__name='rigging')
        context['sound_light'] = Event.objects.get(pk=self.get_object().pk).technicians.filter(
            groups__name='sound_light')
        return context
