# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

def about(request):
    return render(request, template_name = 'about.html', context={ 'name': request.user.username })

def rating(request):
    return render(request, template_name='rating.html', context={'name': request.user.username})

def help_request(request):
    return render(request, template_name='help_request.html', context={'name': request.user.username})

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
                return HttpResponse('К сожалению, аккаунт не существует. <button><a href="/">Вернуться назад</a></button>')
        else:
            return redirect('/login_page/', permanent=False)
    elif request.method=='POST' and request.POST['action']=='logout':
        logout(request)
        return render(request,'login_page.html',context={})
    else:#if request.method=='GET':
        return render(request,'login_page.html', context={ 'name': request.user.username })