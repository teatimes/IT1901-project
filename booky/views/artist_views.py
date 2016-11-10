import json
from urllib import request, error

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from booky.common import BaseMixin, has_group, get_artist_user
from booky.forms import ArtistFilter, ArtistCreateForm, ArtistUpdateForm
from booky.models import Artist, Genre, ArtistUser



class ArtistCreate(BaseMixin, CreateView):
    """
            Renders ArtistCreateFrom to user.

        dispatch
        --------
        Checks if user is affiliated with director or manager group,
            if not: return to home view

        form_valid:
        -----------
        if Custom user input with:
            name, genre and booking_fee
        if Last.fm input:
            name, genre, booking_fee, mbid, artist_info, album_info.
            Will also generate setlist from mbid.
        - Creates two new users affiliated with artist,one for band "lorem_ipsum" and one manager "lorem_ipsum_m"

    """
    queryset = Artist.objects.all()
    template_name = 'artist/artist_form.html'

    success_url = "/artists/"
    form_class = ArtistCreateForm

    # Limiting creation of new Artist to Directors and Managers
    def dispatch(self, request, *args, **kwargs):
        if not (has_group(self.request.user, 'director') or has_group(self.request.user, 'manager')):
            return HttpResponseRedirect('/artists/')
        else:
            return super(ArtistCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Getting the data from the form
        data = form.cleaned_data

        # The email-adress to the manager
        form.instance.manager_email = 'ellanezuddi-0390@yopmail.com'

        # Add genre
        obj, created = Genre.objects.get_or_create(name=data['genre'])
        form.instance.genre = obj

        # Add artist and album info
        form.instance.artist_info = data['artist_info']
        form.instance.album_info = data['album_info']

        # Add setlist info
        if data['mbid'] != '':
            try:
                url = "https://api.setlist.fm/rest/0.1/search/setlists.json?artistMbid={}&countryCode=no".format(
                    data['mbid'])
                response = request.urlopen(url)
            except error.URLError:
                pass
            else:
                setlist = json.loads(response.read().decode())['setlists']['setlist']
                if isinstance(setlist, dict):
                    setlist = [setlist]
                form.instance.setlist_info = json.dumps(setlist)

        un = data['name'].replace(' ', '_')
        un = un.lower()

        response = super(ArtistCreate, self).form_valid(form)

        # Create member and manager users
        member, created = User.objects.get_or_create(username=un)
        manager, created = User.objects.get_or_create(username=un + '_m')
        member.set_password('123qwe123qwe')
        manager.set_password('123qwe123qwe')
        member.save()
        manager.save()

        member_user, created = ArtistUser.objects.get_or_create(user_id=member.id, artist_id=self.object.id,
                                                                is_manager=False)
        manager_user, created = ArtistUser.objects.get_or_create(user_id=manager.id, artist_id=self.object.id,
                                                                 is_manager=True)
        member_user.save()
        manager_user.save()

        return response


class ArtistList(BaseMixin, ListView):
    """
            Renders artist context to users.

        dispatch
        --------
        Checks if user is not affiliated with director, manager, organizer or admin group,
            if true:
                redirect home


        get_queryset:
        -------------
        Checks if a GET query has been sent with url, if it's named 'query',
        set new queryset to filter on objects with names that contains that query.


        get_context_data:
        -----------------
        Sends ArtistFilter as artist_form context to use as search field.

    """
    queryset = Artist.objects.all()
    template_name = 'artist/artist_list.html'

    # Sending bandusers and Technicians home
    def dispatch(self, request, *args, **kwargs):
        if not (has_group(self.request.user, 'director') or has_group(self.request.user, 'manager') or has_group(
                self.request.user, 'organizer') or request.user.is_superuser):
            return HttpResponseRedirect('/')
        else:
            return super(ArtistList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset

        # Get stage, genre and semester
        query = self.request.GET.get('query') or ''

        # Filter by search query
        queryset = queryset.filter(name__icontains=query).order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArtistList, self).get_context_data(**kwargs)
        context['artist_form'] = ArtistFilter(self.request.GET or None)
        return context



class ArtistDetail(BaseMixin, DetailView):
    """
        Renders ArtistDetail context to users.

    dispatch
    --------
    Checks if user is affiliated with technician group or a artist user not themselves,
        if true:
            redirect home

    get_context_data:
    -----------------

    if user is artist user, send a boolean for change in templates
    returns upcoming and old events affiliated with artist

    """
    queryset = Artist.objects.all()
    template_name = 'artist/artist_detail.html'

    # Sending Artist not themself and Technicians home
    def dispatch(self, request, *args, **kwargs):
        user_artist = get_artist_user(request.user)
        if user_artist:
            if user_artist.artist_id != self.get_object().id:
                return HttpResponseRedirect('/')
            else:
                return super(ArtistDetail, self).dispatch(request, *args, **kwargs)
        elif has_group(request.user, 'technician'):
            return HttpResponseRedirect('/')
        else:
            return super(ArtistDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArtistDetail, self).get_context_data(**kwargs)
        context['upcomming'] = self.get_object().event_set.filter(status=4, date__gte=timezone.now())
        context['old'] = self.get_object().event_set.filter(status=4, date__lte=timezone.now())
        # Don't need to check if the corresponding artist is self since it's done in dispatch
        if get_artist_user(self.request.user):
            context['self'] = True

        return context
