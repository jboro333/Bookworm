# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.Editor)
admin.site.register(models.AdminGenre)
admin.site.register(models.UserGenre)
admin.site.register(models.Author)
admin.site.register(models.Series)
admin.site.register(models.Book)
admin.site.register(models.Part)
admin.site.register(models.GenreScore)
