# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

MAIN_TEMPLATE = 'Main.html'

# Create your views here.
def get_stream_url(request):

    main_html_dict = {'current_time' : str(datetime.now())}
    
    #return HttpResponse("Stream URL")
    return render(request,
                  MAIN_TEMPLATE,
                  main_html_dict)
