from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from booky.models import Event, ArtistUser


def has_group(user, group_name):
    """
        Parameters
        ----------
        user : User
            User object from django.auth.models
        group_name : str
            string with group name

        Returns
        -------
        boolean
            Return if User has group with group_name

        """
    return user.groups.filter(name=group_name).exists()


def get_artist_user(user):
    """
        Parameters
        ----------
        user : User
            User object from django.auth.models

        Returns
        -------
        ArtistUser
            Return if User has group with group_name

        """
    try:
        return ArtistUser.objects.get(user=user)
    except:
        return None


class BaseMixin(ContextMixin, LoginRequiredMixin):
    """Makes user login to access view classes that uses BaseMixin"""
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        ctx = super(BaseMixin, self).get_context_data(**kwargs)
        ctx['offers'] = Event.objects.all()
        return ctx
