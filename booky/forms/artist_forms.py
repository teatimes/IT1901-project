from django import forms
from booky.models import Artist, Stage


class ArtistFilter(forms.Form):
    query = forms.CharField(required=False)


class ArtistCreateForm(forms.ModelForm):
    genre = forms.CharField(widget=forms.TextInput())
    mbid = forms.CharField(required=False, widget=forms.TextInput(attrs={'hidden': True}))

    class Meta:
        model = Artist
        fields = ('name', 'booking_fee', 'artist_info', 'album_info')
        widgets = {
            'name': forms.TextInput(attrs={'list': 'suggestions', 'autocomplete': 'off'}),
            'artist_info': forms.TextInput(attrs={'hidden': True}),
            'album_info': forms.TextInput(attrs={'hidden': True}),
        }


class ArtistUpdateForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'genre', 'booking_fee')


