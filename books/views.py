# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404


# Create your views here.
def notExists(request):
    raise Http404("Page not found")
