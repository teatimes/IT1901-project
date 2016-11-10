from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView

from booky.common import BaseMixin, has_group
from booky.forms import EventFilter
from booky.models import Event
from booky.views import HomeView


class ResultList(BaseMixin, ListView):
    template_name = 'result_list.html'

    queryset = None

    # Only the director can see what is on the page
    def dispatch(self, request, *args, **kwargs):
        if has_group(request.user, "director") or has_group(request.user, 'organizer'):
            return super(ResultList, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    # Returns the previous events
    def get_queryset(self):
        queryset = Event.objects.filter(status=4, date__lte=timezone.now()).order_by('-date')
        # Filter by stage
        stage = self.request.GET.get('stage') or 'All'
        if stage != 'All':
            queryset = Event.objects.filter(status=4, stage__name=stage, date__lte=timezone.now()).order_by('-date')
        return queryset

    # This is the filter
    def get_context_data(self, **kwargs):
        context = super(ResultList, self).get_context_data(**kwargs)
        context['event_form'] = EventFilter(self.request.GET or None)
        return context



