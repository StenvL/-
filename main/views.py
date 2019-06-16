# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from main.models import DataManager
from openpyxl import Workbook, load_workbook
from main.models import Everything
def about(request):
    '''
    # adding data from file
    wb = load_workbook('data.xlsx')
    ws = wb.active
    for row in (ws.iter_rows(min_row=2, max_col=10, max_row=308)):
        territory_name, planned_length, money, job_type_name, executor_name, year, accident_type, accident_weight, shift_weight, shift_days = row
        DataManager.add_data(territory_name.value, planned_length.value, money.value, job_type_name.value, executor_name.value, year.value, accident_type.value, accident_weight.value, shift_weight.value, shift_days.value)
    '''
    return render(request, template_name = 'about.html', context={ 'name': request.user.username })

def rating(request):
    return render(request, template_name='rating.html', context={'name': request.user.username})

def form(request):
    return render(request, template_name='form.html', context={'name': request.user.username})

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
            return redirect('/login_page', permanent=False)
    elif request.method=='POST' and request.POST['action']=='logout':
        logout(request)
        return render(request,'login_page.html',context={})
    else:#if request.method=='GET':
        return render(request,'login_page.html', context={ 'name': request.user.username })