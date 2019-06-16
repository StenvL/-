# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from main.models import DataManager
from openpyxl import Workbook, load_workbook
from main.models import Everything
from functools import reduce

def about(request):
    # adding data from file
    # wb = load_workbook('data.xlsx')
    # ws = wb.active
    # for row in (ws.iter_rows(min_row=2, max_col=10, max_row=308)):
    #     territory_name, planned_length, money, job_type_name, executor_name, year, accident_type, accident_weight, shift_weight, shift_days = row
    #     DataManager.add_data(territory_name.value, planned_length.value, money.value, job_type_name.value, executor_name.value, year.value, accident_type.value, accident_weight.value, shift_weight.value, shift_days.value)
    return render(request, template_name = 'about.html', context={ 'name': request.user.username })

def rating(request):
    def getData(orgData):
        orgProjectNames = set((list(map(lambda x: x.territory_name, orgData))))
        maxCost = max(list(map(lambda x: x.money, orgData)))
        maxAccCountInProc = max(list(map(lambda x: x.accident_weight, orgData)))

        # print('orgData = '+ str(len(orgData)))
        # print('orgProjectNames = '+ str(orgProjectNames))
        # print('maxAccInProc = '+ str(maxAccCountInProc))  

        result = []

        for orgProjectName in orgProjectNames:
            #print(orgProjectName)

            projectRecords = list(filter(lambda x: x.territory_name == orgProjectName, orgData))            
            
            inProcAccRecords = list(filter(lambda x: x.accident_type == 'В процессе', projectRecords))          
            #print('inProcAccRecords = ' + str(len(inProcAccRecords)))
            
            inResultAccRecords = list(filter(lambda x: x.accident_type == 'По результату', projectRecords))
            #print('inResultAccRecords = ' + str(len(inResultAccRecords)))

            # print(len(inResultAccRecords))
            # print(list(map(lambda x: x.accident_weight, inResultAccRecords)))

            # print(len(inProcAccRecords))
            # print(list(map(lambda x: x.accident_weight, inProcAccRecords)))

            projectData = [
                projectRecords[0].money / maxCost * 100,
                len(inProcAccRecords),
                reduce(lambda a, x: a + x, list(map(lambda x: x.accident_weight, inProcAccRecords)), 0) / 1 if len(inProcAccRecords) == 0 else len(inProcAccRecords),
                len(inResultAccRecords),
                reduce(lambda a, x: a + x, list(map(lambda x: x.accident_weight, inResultAccRecords)), 0) / 1 if len(inResultAccRecords) == 0 else len(inResultAccRecords)
            ]

            #print(projectData)
            result.append(projectData)
        
        maxInProcAccCount = max(list(map(lambda x: x[1], result)))
        maxInResultAccCount = max(list(map(lambda x: x[3], result)))
        for resultItem in result:
            resultItem[1] = resultItem[1] / (maxInProcAccCount / 100)
            resultItem[3] = resultItem[3] / (maxInResultAccCount / 100)

        return result

    from main.models import Everything 
    def normalize():
        result = []

        data = Everything.objects.all()
        tender = list(filter(lambda x: x.territory_name == 'Благоустройство 21', data))[0]
        print(tender.money)

        orgNames = list(filter(lambda x: x != '0', set(list(map(lambda x: x.executor_name, data)))))
        print(orgNames)

        for orgName in orgNames:
            print(orgName)
            orgData = list(filter(lambda x: x.executor_name == orgName, data))

            ratingData = getData(orgData)
            orgQuality = reduce(lambda a, x: a + x[0] / (x[1] * x[2] + x[3] * x[4]), ratingData, 0) / len(ratingData)

            orgExperience = len(
                list(
                    filter(lambda z: z > tender.money * 0.7,
                    set(list(map(lambda x: x.money, orgData))))
                )
            )

            result.append([orgName, orgQuality, orgExperience])
        
        # Массив массивов со структурой [Название компании, Качество, Опыт]
        print(result)
        return result

    normalize()
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