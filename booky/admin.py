from django.contrib import admin
from booky.models import Event, Genre, Artist, Stage

"""Makes these models accessible in admin view"""
admin.site.register(Event)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Stage)
