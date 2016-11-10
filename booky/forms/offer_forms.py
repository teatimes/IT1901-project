from django import forms
from booky.models import Event


class OfferForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = {'artist', 'stage', 'date', 'offer'}

    # Called when submit pushed
    def clean(self):
        cleaned_data = self.cleaned_data
        artist = cleaned_data.get("artist")
        stage = cleaned_data.get("stage")
        date = cleaned_data.get("date")

        # List filtered on objects with same date or stage to prevent double booking
        date_and_stage = Event.objects.filter(date=date, stage=stage)
        # List filtered on objects with same artist and date to prevent double booking
        artist_and_date = Event.objects.filter(artist=artist, date=date)
        message = ""
        if len(date_and_stage) > 1 or len(artist_and_date) > 1:
            for event in date_and_stage:
                # If it is pending or sent
                if event.status == 0 or event.status == 2:
                    message = "Det eksisterer et tilbud på samme scene og dato som per dags dato ikke er godkjent av bookingsjef og/eller band manager."
                # If accepted
                elif event.status == 3 or event.status == 4:
                    message = "Det eksisterer et tilbud på samme scene og dato som er godkjent, men ikke publisert."
                # If length on message is bigger than 0, raise a validationError and show the error message
                if len(message) > 0:
                    raise forms.ValidationError(message)

            for event in artist_and_date:
                # If it is pending, or sent
                if event.status == 0 or event.status == 2:
                    message = "Det eksisterer et tilbud for bandet på gitt dato som per dags dato ikke er godkjent av bookingsjef og/eller band manager."
                # If accepted
                elif event.status == 3 or event.status == 4:
                    message = "Det eksisterer et tilbud for bandet på gitt dato som er godkjent, men ikke publisert."
                # If length on message is bigger than 0, raise a validationError and show the error message
                if len(message) > 0:
                    raise forms.ValidationError(message)
        return self.cleaned_data
