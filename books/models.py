# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Editor(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class AdminGenre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class UserGenre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, blank=False, null=False)

    def __unicode__(self):
        return "%s (by %s)" % (self.name, self.user)


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateField(auto_now=False, auto_now_add=False)
    language = models.CharField(max_length=20)

    def __unicode__(self):
        return self.title


# Relationships
class Part(models.Model):  # Restriction: only one series per book (not implemented)
    book = models.ForeignKey(Book, blank=False, null=False)
    series = models.ForeignKey(Series, blank=False, null=False)
    number = models.IntegerField()

    def __unicode__(self):
        return "%s (%s #%d)" % (self.book, self.series, self.number)


class GenreScore(models.Model):
    book = models.ForeignKey(Book, blank=False, null=False)
    genre = models.ForeignKey(AdminGenre, blank=False, null=False)
    # user = models.ForeignKey(User, blank=False, null=False)

    def __unicode__(self):
        return "%s - %s" % (self.book, self.genre)
