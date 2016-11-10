import json
import math

from django import template
from django.contrib.auth.models import Group

from booky.common import get_artist_user

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
        Filter function to see if user is affiliated with group
    :param user: User
        Standard user object
    :param group_name: string
        String of group name you want to search for
    :return: boolean
        if User is affiliated with Group that is named group_name
    """
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

@register.filter(name='listify')
def listify(string):
    """
        Takes string, splits on \n and retruns as html unordered list
    :param string:
        Textstring that is to be splitted
    :return: string
        Retruns string with hotml formated list.
    """
    html = "<ul class='listify-list'>"
    for item in string.split('\n'):
        if str(item) is not '':
            html += '<li>' + str(item) + '</li>'
    html += '</ul>'
    return html

@register.simple_tag(takes_context=True)
def calc_ticket_price(context):
    """
        Calculates how much the ticked price should be to break even if there is 60% attendance
    :param context: Event
        Event object that is used to get booking_fee of artist, cost and capacity of stage.
    :return: Integer
        Calculated value to break even at 60% capacity

    """
    obj = context['object']
    price = (obj.artist.booking_fee + obj.stage.cost + 10000) / (obj.stage.capacity * 0.7)
    return int(math.ceil(price / 100.0)) * 100

@register.simple_tag()
def get_profitt(event):
    """
        Calculates the profitt of the concert
    :param event: Event
        Event object uesd to get artist.booking_fee, attendance and ticket_price
    :return: Integer
        How much is earned after you removed the cost of artist and stage cost.
    """
    return (event.attendance * event.ticket_price) - (event.artist.booking_fee + event.stage.cost)

@register.simple_tag()
def get_artist_image(artist, size='medium'):
    """
        Gets image out of artist.artist_info
    :param artist: Artist
        Used to fetch that objects artist_info
    :param size: string
        Unless spessified otherwise, the standard is medium
    :return: string
        URL to image to that artist, if artist hasn't artist_info return stock photo.
    """
    if artist.artist_info:
        info = json.loads(artist.artist_info)
        return next(img['#text'] for img in info['image'] if img['size'] == size)
    else:
        return 'http://pre01.deviantart.net/cbf8/th/pre/i/2014/019/2/3/autumn_blur___free_texture___background_by_supersweetstock-d72t65j.jpg'


@register.filter(name='is_artist_manager')
def is_artist_manager(user):
    """
        Checks if user is ArtistManager
    :param user: User

    :return: boolean
        Returns True or False if get_artist_user returns somthing and it has is_managar to True
    """
    return get_artist_user(user) and get_artist_user(user).is_manager

@register.filter(name='is_band_user')
def is_band_user(user):
    """
        Checks if user is Affiliated with band user
    :param user: User

    :return: boolean
        Retruns true if get_artist_user retruned not none
    """
    return get_artist_user(user) is not None