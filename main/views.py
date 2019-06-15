# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, template_name = 'basic.html')

def about(request):
    return render(request, template_name = 'about.html')

def login_page(request):
    if request.method=='POST' and request.POST['action']=='login':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('We are sorry. Account disabled. Connect website administrator. <button><a href="/">Back to site</a></button>')
        else:
            return redirect('/login_page/', permanent=False)
    elif request.method=='POST' and request.POST['action']=='logout':
        logout(request)
        return render(request,'login_page.html',context={})
    else:#if request.method=='GET':
        return render(request,'login_page.html',context={})