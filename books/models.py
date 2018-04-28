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
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class UserGenre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s (by %s)" % (self.name, self.user)


class Author(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)

    def __unicode__(self):
        name = self.name.split()
        if (len(name) >= 3):
            return "%s %s, %s" % (name[-2], name[-1], " ".join(name[:-2]))
        return "%s, %s" % (name[1], name[0])


class Series(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    editor = models.ManyToManyField(Editor)
    pub_date = models.DateField(auto_now=False, auto_now_add=False, blank=True,
                                null=True)
    language = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.author)


# Relationships
class Part(models.Model):
    book = models.ForeignKey(Book)
    series = models.ForeignKey(Series)
    number = models.IntegerField()

    def __unicode__(self):
        return "%s (%s #%d)" % (self.book, self.series, self.number)

    class Meta:
        unique_together = (('series', 'number'))


class GenreScore(models.Model):
    book = models.ForeignKey(Book)
    genre = models.ForeignKey(AdminGenre)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s - %s - %s" % (self.book, self.genre, self.user)

    class Meta:
        unique_together = (('book', 'genre', 'user'))


class BookScore(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    score = models.IntegerField()
    text = models.TextField()

    def __unicode__(self):
        return "%s - %s (%s)" % (self.user, self.book, self.score)

    class Meta:
        unique_together = (('book', 'user'))
