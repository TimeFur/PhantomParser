# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from models import *
import os

MAIN_TEMPLATE = 'Main.html'

def DB_practice():
    #CRUD concept

    #Create
    Stream_DB.objects.create(title = "_Practice",
                             url = "www.youtube.com",
                             photo = "static\img\XXX.jpg")
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
    print "get_stream_url"
    #DB_practice()
    main_html_dict = {'current_time' : str(datetime.now())}
    
    return HttpResponse("Stream URL")
    '''
    return render(request,
                  MAIN_TEMPLATE,
                  main_html_dict)
    '''
def home_page(request):
    print "home_page"
    
    #f = Stream_DB.objects.filter(title = "Little Doll")
    #f[0].delete()
    f = Stream_DB.objects.filter(title = "Little Doll")
    print f
    #f[0].delete()
    
    print "Current path " + os.getcwd()
    db_data = Stream_DB.objects.all()
    main_html_dict = {'DB' : db_data}
    return render(request,
                  MAIN_TEMPLATE,
                  main_html_dict)

def get_partial_model(request, pk):
    print "get_partial_model"
    print "~~~~~GET pk = " , pk, type(pk)
    data = Stream_DB.objects.filter(title = "Little Doll")
    main_html_dict = {'DB' : data}

    
    
    return render(request,
                  MAIN_TEMPLATE,
                  main_html_dict)





    
    
