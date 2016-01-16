# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 23:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import overspill.talks.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField(blank=True, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_from', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255)),
                ('title', models.CharField(max_length=200)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('image', models.ImageField(max_length=255, upload_to=overspill.talks.helpers.set_slide_image_url)),
                ('notes', models.TextField(blank=True)),
                ('audio', models.FileField(blank=True, max_length=255, upload_to=overspill.talks.helpers.set_slide_audio_url)),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('speaker_name', models.CharField(blank=True, max_length=100)),
                ('slideshow', models.FileField(max_length=255, upload_to=overspill.talks.helpers.set_talk_slideshow_url)),
                ('uploaded', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[(b'p', 'pre-processing'), (b'e', 'errored'), (b'u', 'published'), (b'o', 'post-processing')], max_length=1)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talks', to='talks.Event')),
            ],
            options={
                'ordering': ('-uploaded', 'slug'),
            },
        ),
        migrations.AddField(
            model_name='slide',
            name='talk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='talks.Talk'),
        ),
        migrations.AddField(
            model_name='link',
            name='talk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='talks.Talk'),
        ),
        migrations.AlterUniqueTogether(
            name='talk',
            unique_together=set([('slug', 'event')]),
        ),
        migrations.AlterUniqueTogether(
            name='slide',
            unique_together=set([('number', 'talk')]),
        ),
    ]