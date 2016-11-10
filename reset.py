import os
import shutil

from django.core.management import execute_from_command_line


data = '[{"model": "contenttypes.contenttype", "pk": 1, "fields": {"app_label": "admin", "model": "logentry"}}, {"model": "contenttypes.contenttype", "pk": 2, "fields": {"app_label": "auth", "model": "group"}}, {"model": "contenttypes.contenttype", "pk": 3, "fields": {"app_label": "auth", "model": "permission"}}, {"model": "contenttypes.contenttype", "pk": 4, "fields": {"app_label": "auth", "model": "user"}}, {"model": "contenttypes.contenttype", "pk": 5, "fields": {"app_label": "contenttypes", "model": "contenttype"}}, {"model": "contenttypes.contenttype", "pk": 6, "fields": {"app_label": "sessions", "model": "session"}}, {"model": "contenttypes.contenttype", "pk": 7, "fields": {"app_label": "booky", "model": "stage"}}, {"model": "contenttypes.contenttype", "pk": 8, "fields": {"app_label": "booky", "model": "genre"}}, {"model": "contenttypes.contenttype", "pk": 9, "fields": {"app_label": "booky", "model": "artist"}}, {"model": "contenttypes.contenttype", "pk": 10, "fields": {"app_label": "booky", "model": "event"}}, {"model": "sessions.session", "pk": "03h3quien4dfbq0isqnbmxv6i6dig2na", "fields": {"session_data": "OWVlNTJiMjA1Mzg0MWYyNzkzODlkYjEzYzcyZDcxNmE2YWMzYWQ4ODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTdmY2FiODZiMTllMTIxZmFkZDI3Y2I3YjhiYmQ2NmMzMThlNTk4In0=", "expire_date": "2016-10-30T15:12:09.958Z"}}, {"model": "booky.stage", "pk": 1, "fields": {"name": "Storsalen", "capacity": 1000, "cost": 20000}}, {"model": "booky.stage", "pk": 2, "fields": {"name": "Knaus", "capacity": 100, "cost": 7500}}, {"model": "booky.stage", "pk": 3, "fields": {"name": "Edgar", "capacity": 100, "cost": 5000}}, {"model": "booky.stage", "pk": 4, "fields": {"name": "Klubben", "capacity": 100, "cost": 5000}}, {"model": "booky.stage", "pk": 5, "fields": {"name": "Bodegaen", "capacity": 200, "cost": 5000}}, {"model": "auth.permission", "pk": 1, "fields": {"name": "Can add log entry", "content_type": 1, "codename": "add_logentry"}}, {"model": "auth.permission", "pk": 2, "fields": {"name": "Can change log entry", "content_type": 1, "codename": "change_logentry"}}, {"model": "auth.permission", "pk": 3, "fields": {"name": "Can delete log entry", "content_type": 1, "codename": "delete_logentry"}}, {"model": "auth.permission", "pk": 4, "fields": {"name": "Can add group", "content_type": 2, "codename": "add_group"}}, {"model": "auth.permission", "pk": 5, "fields": {"name": "Can change group", "content_type": 2, "codename": "change_group"}}, {"model": "auth.permission", "pk": 6, "fields": {"name": "Can delete group", "content_type": 2, "codename": "delete_group"}}, {"model": "auth.permission", "pk": 7, "fields": {"name": "Can add permission", "content_type": 3, "codename": "add_permission"}}, {"model": "auth.permission", "pk": 8, "fields": {"name": "Can change permission", "content_type": 3, "codename": "change_permission"}}, {"model": "auth.permission", "pk": 9, "fields": {"name": "Can delete permission", "content_type": 3, "codename": "delete_permission"}}, {"model": "auth.permission", "pk": 10, "fields": {"name": "Can add user", "content_type": 4, "codename": "add_user"}}, {"model": "auth.permission", "pk": 11, "fields": {"name": "Can change user", "content_type": 4, "codename": "change_user"}}, {"model": "auth.permission", "pk": 12, "fields": {"name": "Can delete user", "content_type": 4, "codename": "delete_user"}}, {"model": "auth.permission", "pk": 13, "fields": {"name": "Can add content type", "content_type": 5, "codename": "add_contenttype"}}, {"model": "auth.permission", "pk": 14, "fields": {"name": "Can change content type", "content_type": 5, "codename": "change_contenttype"}}, {"model": "auth.permission", "pk": 15, "fields": {"name": "Can delete content type", "content_type": 5, "codename": "delete_contenttype"}}, {"model": "auth.permission", "pk": 16, "fields": {"name": "Can add session", "content_type": 6, "codename": "add_session"}}, {"model": "auth.permission", "pk": 17, "fields": {"name": "Can change session", "content_type": 6, "codename": "change_session"}}, {"model": "auth.permission", "pk": 18, "fields": {"name": "Can delete session", "content_type": 6, "codename": "delete_session"}}, {"model": "auth.permission", "pk": 19, "fields": {"name": "Can add stage", "content_type": 7, "codename": "add_stage"}}, {"model": "auth.permission", "pk": 20, "fields": {"name": "Can change stage", "content_type": 7, "codename": "change_stage"}}, {"model": "auth.permission", "pk": 21, "fields": {"name": "Can delete stage", "content_type": 7, "codename": "delete_stage"}}, {"model": "auth.permission", "pk": 22, "fields": {"name": "Can add genre", "content_type": 8, "codename": "add_genre"}}, {"model": "auth.permission", "pk": 23, "fields": {"name": "Can change genre", "content_type": 8, "codename": "change_genre"}}, {"model": "auth.permission", "pk": 24, "fields": {"name": "Can delete genre", "content_type": 8, "codename": "delete_genre"}}, {"model": "auth.permission", "pk": 25, "fields": {"name": "Can add artist", "content_type": 9, "codename": "add_artist"}}, {"model": "auth.permission", "pk": 26, "fields": {"name": "Can change artist", "content_type": 9, "codename": "change_artist"}}, {"model": "auth.permission", "pk": 27, "fields": {"name": "Can delete artist", "content_type": 9, "codename": "delete_artist"}}, {"model": "auth.permission", "pk": 28, "fields": {"name": "Can add event", "content_type": 10, "codename": "add_event"}}, {"model": "auth.permission", "pk": 29, "fields": {"name": "Can change event", "content_type": 10, "codename": "change_event"}}, {"model": "auth.permission", "pk": 30, "fields": {"name": "Can delete event", "content_type": 10, "codename": "delete_event"}}, {"model": "auth.group", "pk": 1, "fields": {"name": "director", "permissions": []}}, {"model": "auth.group", "pk": 2, "fields": {"name": "manager", "permissions": []}}, {"model": "auth.group", "pk": 3, "fields": {"name": "organizer", "permissions": []}}, {"model": "auth.group", "pk": 4, "fields": {"name": "technician", "permissions": []}}, {"model": "auth.user", "pk": 1, "fields": {"password": "pbkdf2_sha256$30000$W0HE4DJSgP1H$s1xdPrisgiWbiYCpEj6OGGwdTH2id1d3yA/5EgNP8EU=", "last_login": "2016-10-16T15:12:09.955Z", "is_superuser": true, "username": "admin", "first_name": "", "last_name": "", "email": "", "is_staff": true, "is_active": true, "date_joined": "2016-10-16T15:11:45.330Z", "groups": [], "user_permissions": []}}, {"model": "auth.user", "pk": 2, "fields": {"password": "pbkdf2_sha256$30000$CJT0oAo8CzHx$2o+TTZVU1DPMmg5Q6AmCDyLPp8pnOaDbe0YngQ3chvs=", "last_login": null, "is_superuser": false, "username": "director", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2016-10-16T15:12:56.947Z", "groups": [1], "user_permissions": []}}, {"model": "auth.user", "pk": 3, "fields": {"password": "pbkdf2_sha256$30000$g2EHZMo7xv9S$aq9G+CP6N4A0NP0eC0JUbOFuC/hSpHWt40fJEJNFg0w=", "last_login": null, "is_superuser": false, "username": "manager_1", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2016-10-16T15:18:52.908Z", "groups": [2], "user_permissions": []}}, {"model": "auth.user", "pk": 4, "fields": {"password": "pbkdf2_sha256$30000$DjMSGC7L4KRL$kRKX/ptFSvb9xxkg4gQywx66HnNz5w9QjyfRuVEKGgE=", "last_login": null, "is_superuser": false, "username": "manager_2", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2016-10-16T15:19:02.920Z", "groups": [2], "user_permissions": []}}, {"model": "auth.user", "pk": 5, "fields": {"password": "pbkdf2_sha256$30000$fsfKqSWyuujV$UDJNDZKyPDpsak+RdQzd0QnSW/S5f+WyJSXv6QY5Dc8=", "last_login": null, "is_superuser": false, "username": "tech_1", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2016-10-16T15:19:42.365Z", "groups": [4], "user_permissions": []}}, {"model": "auth.user", "pk": 6, "fields": {"password": "pbkdf2_sha256$30000$mqodL94FEOlI$tXMWZCeUJyE/z4O0oRY7X1kZa26GJuG6K6+gt8VqH2s=", "last_login": null, "is_superuser": false, "username": "tech_2", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2016-10-16T15:19:51.243Z", "groups": [4], "user_permissions": []}}, {"model": "auth.user", "pk": 7, "fields": {"password": "pbkdf2_sha256$30000$MSfiFJzk1zB4$yne5KWPIi1Ait3Jkgb4oKRx1IshGod8/Z5FbhnLzzi8=", "last_login": null, "is_superuser": false, "username": "organizer", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2016-10-16T15:20:17.628Z", "groups": [3], "user_permissions": []}}, {"model": "admin.logentry", "pk": 1, "fields": {"action_time": "2016-10-16T15:12:57.053Z", "user": 1, "content_type": 4, "object_id": "2", "object_repr": "director", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 2, "fields": {"action_time": "2016-10-16T15:18:53.012Z", "user": 1, "content_type": 4, "object_id": "3", "object_repr": "manager_1", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 3, "fields": {"action_time": "2016-10-16T15:19:03.021Z", "user": 1, "content_type": 4, "object_id": "4", "object_repr": "manager_2", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 4, "fields": {"action_time": "2016-10-16T15:19:42.467Z", "user": 1, "content_type": 4, "object_id": "5", "object_repr": "tech_1", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 5, "fields": {"action_time": "2016-10-16T15:19:51.351Z", "user": 1, "content_type": 4, "object_id": "6", "object_repr": "tech_2", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 6, "fields": {"action_time": "2016-10-16T15:19:56.631Z", "user": 1, "content_type": 4, "object_id": "6", "object_repr": "tech_2", "action_flag": 2, "change_message": "[]"}}, {"model": "admin.logentry", "pk": 7, "fields": {"action_time": "2016-10-16T15:20:17.728Z", "user": 1, "content_type": 4, "object_id": "7", "object_repr": "organizer", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 8, "fields": {"action_time": "2016-10-16T15:21:04.755Z", "user": 1, "content_type": 2, "object_id": "1", "object_repr": "director", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 9, "fields": {"action_time": "2016-10-16T15:21:08.889Z", "user": 1, "content_type": 2, "object_id": "2", "object_repr": "manager", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 10, "fields": {"action_time": "2016-10-16T15:21:15.294Z", "user": 1, "content_type": 2, "object_id": "3", "object_repr": "organizer", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 11, "fields": {"action_time": "2016-10-16T15:21:23.824Z", "user": 1, "content_type": 2, "object_id": "4", "object_repr": "technician", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 12, "fields": {"action_time": "2016-10-16T15:21:37.094Z", "user": 1, "content_type": 4, "object_id": "2", "object_repr": "director", "action_flag": 2, "change_message": "[]"}}, {"model": "admin.logentry", "pk": 13, "fields": {"action_time": "2016-10-16T15:21:45.781Z", "user": 1, "content_type": 4, "object_id": "3", "object_repr": "manager_1", "action_flag": 2, "change_message": "[]"}}, {"model": "admin.logentry", "pk": 14, "fields": {"action_time": "2016-10-16T15:21:57.461Z", "user": 1, "content_type": 4, "object_id": "4", "object_repr": "manager_2", "action_flag": 2, "change_message": "[]"}}, {"model": "admin.logentry", "pk": 15, "fields": {"action_time": "2016-10-16T15:22:09.658Z", "user": 1, "content_type": 4, "object_id": "7", "object_repr": "organizer", "action_flag": 2, "change_message": "[]"}}, {"model": "admin.logentry", "pk": 16, "fields": {"action_time": "2016-10-16T15:22:17.562Z", "user": 1, "content_type": 4, "object_id": "5", "object_repr": "tech_1", "action_flag": 2, "change_message": "[]"}}, {"model": "admin.logentry", "pk": 17, "fields": {"action_time": "2016-10-16T15:22:26.062Z", "user": 1, "content_type": 4, "object_id": "6", "object_repr": "tech_2", "action_flag": 2, "change_message": "[]"}}, {"model": "admin.logentry", "pk": 18, "fields": {"action_time": "2016-10-16T15:24:01.065Z", "user": 1, "content_type": 7, "object_id": "1", "object_repr": "Storsalen", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 19, "fields": {"action_time": "2016-10-16T15:24:13.318Z", "user": 1, "content_type": 7, "object_id": "2", "object_repr": "Knaus", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 20, "fields": {"action_time": "2016-10-16T15:31:49.008Z", "user": 1, "content_type": 7, "object_id": "3", "object_repr": "Edgar", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 21, "fields": {"action_time": "2016-10-16T15:32:01.058Z", "user": 1, "content_type": 7, "object_id": "4", "object_repr": "Klubben", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 22, "fields": {"action_time": "2016-10-16T15:32:24.447Z", "user": 1, "content_type": 7, "object_id": "5", "object_repr": "Bodegaen", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}]'


migrations1 = '''
# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-16 15:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, unique=True)),
                ('manager_email', models.EmailField(max_length=254, null=True)),
                ('booking_fee', models.IntegerField(default=0)),
                ('artist_info', models.TextField(blank=True, null=True)),
                ('album_info', models.TextField(blank=True, null=True)),
                ('setlist_info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(null=True)),
                ('date', models.DateField(null=True)),
                ('ticket_price', models.IntegerField(default=0)),
                ('attendance', models.IntegerField(default=0)),
                ('status', models.IntegerField(choices=[(0, 'pending approval'), (1, 'declined'), (2, 'sent'), (3, 'accepted'), (4, 'published')], default=0)),
                ('offer', models.TextField(blank=True, null=True)),
                ('artist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booky.Artist')),
                ('creator', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='events_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('capacity', models.IntegerField()),
                ('cost', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booky.Stage'),
        ),
        migrations.AddField(
            model_name='event',
            name='technicians',
            field=models.ManyToManyField(related_name='events_assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artist',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booky.Genre'),
        ),
    ]

'''

migrations2 = '''
# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-24 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booky', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='requirements',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='setlist',
            field=models.TextField(blank=True, null=True),
        ),
    ]

'''

migrations3 = '''
# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 10:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booky', '0002_auto_20161024_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_manager', models.BooleanField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booky.Artist')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

'''


root = os.path.dirname(__file__)
shutil.copy(os.path.join(root, 'db_clean.sqlite3'), os.path.join(root, 'db.sqlite3'))

path = os.path.join(root, 'booky/migrations')

if os.path.exists(path):
    shutil.rmtree(path)

os.makedirs(path, exist_ok=True)

f = open(os.path.join(path, '__init__.py'), mode='w')
f.close()

f = open(os.path.join(path, '0001_initial.py'), mode='w')
f.write(migrations1)
f.close()

f = open(os.path.join(path, '0002_auto_20161024_1510.py'), mode='w')
f.write(migrations2)
f.close()

f = open(os.path.join(path, '0003_artistuser.py'), mode='w')
f.write(migrations3)
f.close()



# execute_from_command_line(["python django-admin", "loaddata data.json"])