# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from models import *

MAIN_TEMPLATE = 'Main.html'

def DB_practice():
    #CRUD concept

    #Create
    Stream_DB.objects.create(title = "_Practice",
                             url = "www.youtube.com",
                             photo = "./Photo/img1.jpg")
    #Read
    show_db = Stream_DB.objects.all()
    print show_db[0].url
    
    #Update
    filter_db = Stream_DB.objects.filter(title = "_Practice")
    filter_db.update(url = "www.yahoo.com")
    print show_db[0].url
    
    #Delete
    filter_db.delete()
    print show_db
    
# Create your views here.
def get_stream_url(request):
    #DB_practice()
    main_html_dict = {'current_time' : str(datetime.now())}
    
    #return HttpResponse("Stream URL")
    return render(request,
                  MAIN_TEMPLATE,
                  main_html_dict)
