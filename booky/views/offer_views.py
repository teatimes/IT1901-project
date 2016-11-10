import json
import random

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, FormView

from booky.common import BaseMixin, has_group, get_artist_user
from booky.forms.offer_forms import OfferForm
from booky.models import Event


class OfferCreate(BaseMixin, FormView):

    """
        dispatch
        --------
        Checks if user is not affiliated with director or manager
            if true:
                redirect home


        form_valid:
        -------------
        Saves form


        get_context_data:
        -----------------
        Get a context with disabled dates

    """

    queryset = Event.objects.all()
    template_name = 'offer/offer_form.html'
    form_class = OfferForm

    success_url = "/offers/"

    # Denies access to anyone but Directors and Managers
    def dispatch(self, request, *args, **kwargs):
        if not (has_group(self.request.user, 'director') or has_group(self.request.user, 'manager')):
            return HttpResponseRedirect('/offers/')
        else:
            return super(OfferCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super(OfferCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfferCreate, self).get_context_data(**kwargs)
        disabled_dates = {}

        for event in Event.objects.all():
            if event.stage.name not in disabled_dates:
                disabled_dates[event.stage.name] = []
            disabled_dates[event.stage.name].append(event.date.strftime('%d-%m-%Y'))

        context['disableddates'] = json.dumps(disabled_dates)
        return context

class OfferUpdate(BaseMixin, UpdateView):

    """
        dispatch
        --------
        Checks if it is director and offer has status pending or accepted, manager and offer has status sent, or if it is declined,
            if true:
                return HttpResponsRedirect so that they can't edit


        form_valid:
        -------------
        if status is approved:
            send email to manager
        else if status is published:
            add technicians to rigging and sound
        update status

    """

    queryset = Event.objects.all()
    template_name = 'offer/offer_form.html'

    success_url = "/offers/"
    fields = ('artist', 'stage', 'date', 'offer')

    # So users can't edit when they shouldn't, or if the offer is declined
    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().status == 0 or self.get_object().status == 3) and not has_group(self.request.user, 'director'):
            return HttpResponseRedirect('/offer/'+self.kwargs.get('pk')+'/')
        elif self.get_object().status == 2 and not has_group(self.request.user, 'manager'):
            return HttpResponseRedirect('/offer/' + self.kwargs.get('pk') + '/')
        elif self.get_object().status == 1:
            return HttpResponseRedirect('/offer/' + self.kwargs.get('pk') + '/')
        else:
            return super(OfferUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = self.request.POST

        if 'status' in post:
            status = post['status']

            if status == 'approved':
                form.instance.status = 2
                email = EmailMessage('Offer', form.cleaned_data['offer'], to=[form.instance.artist.manager_email])
                email.send()
            elif status == 'declined':
                form.instance.status = 1
            elif status == 'accepted':
                form.instance.status = 3
            elif status == 'published':
                form.instance.status = 4
                form.instance.attendance = int(form.instance.stage.capacity * (random.randint(70, 100) / 100))
                tech_qs = User.objects.filter(groups__name='technician')
                rig = tech_qs.filter(groups__name='rigging').order_by('?')[:2]
                sound_light = tech_qs.filter(groups__name='sound_light').order_by('?')[:2]
                form.instance.technicians.add(*rig)
                form.instance.technicians.add(*sound_light)


        if 'description' in post:
            form.instance.description = post['description']
        if 'ticket_price' in post:
            form.instance.ticket_price = post['ticket_price']

        return super(OfferUpdate, self).form_valid(form)


class OfferList(BaseMixin, ListView):
    """
           dispatch
           --------
           Checks if it is artist but not artist manager, or if techinician,
               if true:
                   return HttpResponsRedirect so that they can't edit


           get_queryset:
           -------------
           if artist is logged in:
               return a list of related offers
           else:
                return a list of all except denied

           get_context_data:
           -----------------
           return context where offers is sorted in different list based on status

       """
    template_name = 'offer/offer_list.html'

    # Artists and todo Technicians not allowed?
    def dispatch(self, request, *args, **kwargs):
        if (get_artist_user(request.user) and not get_artist_user(request.user).is_manager) or has_group(request.user, 'technician'):
            return HttpResponseRedirect('/')
        else:
            return super(OfferList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        # If artist is logged in, only show related offers
        if get_artist_user(self.request.user):
            return Event.objects.filter(status__gte=2, artist__name=get_artist_user(self.request.user).artist.name)
        else:
            return Event.objects.all().order_by('status').exclude(status__in=[1])


    def get_context_data(self, **kwargs):
        context = super(OfferList, self).get_context_data(**kwargs)
        artist = get_artist_user(self.request.user)
        #Added queryset to avoid multiple queries.
        query_set = Event.objects.all()
        context['pending_count'] = len(query_set.filter(status=0))
        context['sent_count'] = len(query_set.filter(status=2))
        context['approved_count'] = len(query_set.filter(status=3))
        context['published_count'] = len(query_set.filter(status=4))
        if artist:
            context['received_count_band'] = len(query_set.filter(status=2, artist__name=artist.artist.name))
            context['accepted_count_band'] = len(query_set.filter(status=3, artist__name=artist.artist.name))
            context['published_count_band'] = len(query_set.filter(status=4, artist__name=artist.artist.name))
        return context


class OfferDetail(BaseMixin, DetailView):
    """
        dispatch:
        ---------

        if manager and sent or director and pending or accepted:
            let them edit offer
        else if it is not an artist related to the offer:
            return to home
        else:
            calls dispatch on the super

    """
    queryset = Event.objects.all()
    template_name = 'offer/offer_detail.html'

    def dispatch(self, request, *args, **kwargs):
        status = self.get_object().status
        # Booking manager can edit when sent (to accepted or declined) or booking director when it is pending, sent or accepted but not published
        if has_group(request.user, 'manager') and status == 2 or \
           has_group(request.user, 'director') and status in (0, 3):
            return redirect('offer-update', pk=self.get_object().pk)
        # Redirect ArtistUsers that isn't connected to the offered artist
        elif get_artist_user(request.user) and get_artist_user(request.user).artist.id is not self.get_object().artist.id:
            return HttpResponseRedirect('/')
        else:
            return super(OfferDetail, self).dispatch(request, *args, **kwargs)



