# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Editor(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    def string(self):
        if (self.name == None):
            return ""
        else:
            return "\t- Editor: " + name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s (by %s)" % (self.name, self.user)
    
    def unicode(self):
        return self.__unicode__()
    
    class Meta:
        unique_together = (('name', 'user'))    


class Author(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)

    def __unicode__(self):
        name = self.name.split()
        if (len(name) >= 3):
            return "%s %s, %s" % (name[-2], name[-1], " ".join(name[:-2]))
        if (len(name) == 2):
            return "%s, %s" % (name[1], name[0])
        return name[0]


class Series(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    editor = models.ForeignKey(Editor, null=True, blank=True)
    pub_date = models.DateField(auto_now=False, auto_now_add=False, blank=True,
                                null=True)
    language = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.author)
    
    def valoration(self):
        points = BookScore.objects.filter(book=self)
        count = 0
        for point in points:
            count += point.score
        if (points.count() != 0):
            return count / float(points.count())
        else:
            return 5.0
    
    def best_genres(self):
        genres = GenreScore.objects.filter(book=self)
        if (genres.count() == 0):
            return []
        
        results = {}
        for genrescore in genres:
            if (genrescore.genre in results):
                results[genrescore.genre] += 1
            else:
                results[genrescore.genre] = 1
        
        lst = [(key, val) for (key, val) in results.items()]
        values = []
        for i in range(5):
            (maxkey, maxval) = (None, 0)
            for (key, val) in lst:
                if (maxval < val):
                    (maxkey, maxval) = (key, val)
            values += [(maxkey, maxval)]
            lst.remove((maxkey, maxval))
            if (lst == []):
                return values
        return values

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
    genre = models.ForeignKey(Genre)
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
