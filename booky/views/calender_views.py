import datetime
import json
import time

from django.views.generic import TemplateView

from booky.common import BaseMixin, get_artist_user
from booky.models import Event


class CalendarView(BaseMixin, TemplateView):
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        #Checking if user is either band member or band manager
        artist = get_artist_user(self.request.user)

        events = []
        offer_list = []
        concert_list = []
        rehearsal_list = []

        def add_event(events, offer_list, concert_list, rehearsal_list,  title, start, status, stage, allDay):

            #Adding event and appending it to events
            event = {"title": title, "start": start, "status": status, "stage": stage, "allDay": allDay}
            events.append(event)

            if artist:    
                #Making date string from the event's timestamp with the formate dd.mm.yyyy
                event_date = datetime.datetime.fromtimestamp(start).strftime('%d.%m.%Y')

                #Offer accepted by band manager or concert published
                if status >= 3:

                    #Create rehearsal and append it to events_list
                    event = {"title": "13.30 - 16.00: " + stage, "start": start, "status": 5, "stage": stage, "allDay": allDay}
                    events.append(event)

                    #Check if the event is scheduled later than the current date
                    if time.time() < start:

                        #Create note for rehearsal and append it to rehearsals_list
                        rehearsal =  event_date + ", 13.30 - 16.00: " + stage
                        rehearsal_list.append(rehearsal)

                        #Create note for concert and append it to concerts_list
                        concerts = event_date + ": " + stage
                        concert_list.append(concerts)

                #Offer sent and awaiting approval by band manager
                else:

                    #Check if the offer is scheduled later than the current date
                    if time.time() < start:

                        #Create note for offer and append it to offers_list
                        offer = event_date + ": " + stage
                        offer_list.append(offer)

        if artist:
            #Events with status offer sent, offer accepted or concert published for the 
            #currently logged in band member or band manager is sorted in ascending order by date
            for event in Event.objects.filter(status__gte=2, artist__name=artist.artist.name).order_by('date'):
                t = datetime.datetime.now().replace(event.date.year, event.date.month, event.date.day)
                add_event(events, offer_list, concert_list, rehearsal_list, event.stage.name, t.timestamp(), event.status, event.stage.name, True)

        else:
            #User is not part of band, and the calendar shows all objects which are not declined
            for event in Event.objects.exclude(status=1):
                t = datetime.datetime.now().replace(event.date.year, event.date.month, event.date.day)
                add_event(events, offer_list, concert_list, rehearsal_list, event.artist.name + " @ " + event.stage.name, t.timestamp(), event.status, event.stage.name, True)

        context['offer_list'] = offer_list
        context['concert_list'] = concert_list
        context['rehearsal_list'] = rehearsal_list
        context['events'] = json.dumps(events)
        return context