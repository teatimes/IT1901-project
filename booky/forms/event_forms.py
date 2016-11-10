from django import forms

from booky.models import Event


class EventFilter(forms.Form):
    # Possible choices on semester
    semester = forms.ChoiceField(choices=[(semester, semester) for semester in ['All', '2016h','2016v', '2015h', '2015v', '2014h', '2014v', '2013h', '2013v']])

    def __init__(self, *args, **kwargs):
        super(EventFilter, self).__init__(*args, **kwargs)
        self.fields['genre'] = forms.ChoiceField(choices=[('All', 'All')] + list(set([(event.artist.genre, event.artist.genre) for event in Event.objects.filter(status=4)])))
        self.fields['stage'] = forms.ChoiceField(choices=[('All', 'All')] + list(set([(event.stage, event.stage) for event in Event.objects.filter(status=4)])))


class RequirementForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('requirements',)