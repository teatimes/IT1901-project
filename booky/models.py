from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Stage(models.Model):
    """
            Stage model, so we can link multiple events on same stages

        Values:
        -------
        name: Char
            Name of stage

        capacity: Integer
            How many people can attend at that stage

        cost: Integer
            The Cost of renting the stage

    """
    name = models.CharField(max_length=200, unique=True)
    capacity = models.IntegerField()
    cost = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
            Genre model for artist, so we can have same genre for different artists

        Values:
        -------
        name: Char
            Name of genre

    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Artist(models.Model):
    """
            Artist model, primary artist model used for this project

        Values:
        -------
        name: Char
            Name of artist

        genre: Genre
            Foreign Key to Genre model

        manager_email: Email
            email to manager, autovalidates so @site.com is needed

        booking_fee: Integer
            The fee that the bad want to play.

        artist_info: Text
            Info about the artist in JSON format, Needs to be converted to | safe before handling.

        album_info: Text
            Info about albums to artist in JSON format,  Needs to be converted to | safe before before handling.

        setlist_info: Text
            Info about concerts artist have had in Norway, Needs to be converted to | safe before handling.

    """

    name = models.CharField(max_length=200, null=True, unique=True)
    genre = models.ForeignKey(Genre, null=True)
    manager_email = models.EmailField(null=True)
    booking_fee = models.IntegerField(default=0)

    artist_info = models.TextField(null=True, blank=True)
    album_info = models.TextField(null=True, blank=True)
    setlist_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class ArtistUser(models.Model):
    """
            ArtistUser, connects User model with certain Artist

        Values:
        -------
        user: User
            ForeignKey to User,

        artist: Artist
            ForeignKey to Artist model

        is_manager: boolean
            if artistUser is the manager account.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist)
    is_manager = models.BooleanField()


class Event(models.Model):
    """
            Event, model that acts like Offer model and Event model for our system


        Values:
        -------
        creator: User
            ForeignKey to User model that created the Event object.

        created: DateTime
            Time field, to show when the offer was created

        artist: Artist
            ForeginKey to link artist to the event, Artist.name is used in combination with Stage.name to make title

        stage: Stage
            ForeginKey to like stage to the event Stage.name is used in combination with Artist.name to make title

        description: Text
            Descrition of the event that is set before it's published

        date: Date
            Date when the event is set to happen, we assume one event will occupy an entire day.

        technicians: User(s)
            ManyToMany relations field for what Users that is supposed to work on that event

        ticket_price: Integer
            price of each ticket for the event

        attendance: Integer
            how many that is going to attend/has attended a event

        status: ChoiceField
            Used to represent the status of the event, given a value from 0 to 4,
            i.e. if an event has status Sent it would have value 2, published value 4.

        offer: Text
            Flavour text that is sent to Artist_Manager when offer is approved by director

        requirements: Text
            Text field that is used to interpreted what artist_manager wants to be done,
            will be slitted on \n and put in a list with filter listify

        setlist: Text
            So artist can list up his/hers/theirs setlist for this event, not yet implemented

        Functions:
        ----------

            get_absolute_url:
            ----------------
                Function to dynamically return the url string to this event object.

            :param None

            :return String
                URL to the EventDetail view of current Event object

    """

    creator = models.ForeignKey(User, default=0, related_name='events_created')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    artist = models.ForeignKey(Artist, null=True)
    stage = models.ForeignKey(Stage, null=True)
    description = models.TextField(null=True)
    date = models.DateField(null=True)
    technicians = models.ManyToManyField(User, related_name='events_assigned')

    ticket_price = models.IntegerField(default=0)
    attendance = models.IntegerField(default=0)

    PENDING_APPROVAL = 0
    DECLINED = 1
    SENT = 2
    ACCEPTED = 3
    PUBLISHED = 4
    STATUS_CHOICES = (
        (PENDING_APPROVAL, 'pending'),
        (DECLINED, 'declined'),
        (SENT, 'sent'),
        (ACCEPTED, 'accepted'),
        (PUBLISHED, 'published')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    offer = models.TextField(null=True, blank=True)

    requirements = models.TextField(null=True, blank=True)
    setlist = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.artist.name + ' @ ' + self.stage.name + ' - ' + str(self.date)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={"pk": self.id})
