# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.shortcuts import render

# # Create your views here.

try: import simplejson as json
except ImportError: import json
import xlwt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from stocks.stockretriever import get_historical_info, get_current_info, get_month_info, get_historical_info_dates, get_last_updated, get_news_feed,Update_database
from stocks.forms import StockForm,QueryForm,DayInfoForm
from stocks.models import Historical,Stock,SymbolInfo
from datetime import datetime

@login_required
def portfolio(request):
    messages=[]
    results=dict()
    if request.method=='POST':
        form=StockForm(request.POST)
        if form.is_valid():
            Handle=form.cleaned_data['Handle'].upper()
            messages=Update_database(Handle)
            result1=Historical.objects.filter(Handle_id=Handle).latest('Date')
            Name = SymbolInfo.objects.filter(Handle=Handle)[0].Name
            results = dict(Name=Name,Handle=result1.Handle_id,High=result1.High,Low=result1.Low,Volume=result1.Volume,Open=result1.Open)
            print results
    form=StockForm()

    return render(request, 'stocks/portfolio.html', {'form': form,
                                                     'infos': [results]})
@login_required
def historical(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['Handle'].upper()
            data = get_historical_info(symbol)
            book = xlwt.Workbook()
            sheet = book.add_sheet('Sheet')
            for i, v in enumerate(data[0].keys()):
                sheet.write(0, i, v)
            for i, row in enumerate(data, start=1):
                for j, v in enumerate(row.values()):
                    sheet.write(i, j, v)
            response = HttpResponse(content_type='application/x-msexcel')
            response['Pragma'] = 'no-cache'
            response['Content-disposition'] = 'attachment; filename=history.xls'
            book.save(response)
            return response

    return render(request, 'stocks/historical.html', {'form': form})

@login_required
def query(request):
    form = QueryForm()
    result=[]
    infos=[]
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            Handle_str = form.cleaned_data['Handle'].upper()
            Handle = SymbolInfo.objects.filter(Handle=Handle_str)[0]
            BeginDatestr = form.cleaned_data['BeginDate']
            EndDatestr = form.cleaned_data['EndDate']
            BeginDate = datetime.strptime(BeginDatestr, "%Y-%m-%d")
            EndDate = datetime.strptime(EndDatestr, "%Y-%m-%d")
        result = Historical.objects.filter(Handle = Handle, Date__lte = EndDate, Date__gte = BeginDate)
        print "Begin Date" + str(BeginDate)
        print "End Date" + str(EndDate)
        print result

    # No results are output if result is [] - if symbol does not exist or
    # dates are incorrect
    return render(request, 'stocks/query.html', {'form': form,
                                                 'infos': result})


@login_required
def symbolInfo(request):
    form = StockForm()
    result=[]
    response = []
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            Handle = form.cleaned_data['Handle'].upper()
        result = SymbolInfo.objects.filter(Handle = Handle)
        response = get_news_feed(Handle)
        print response
    return render(request, 'stocks/symbolInfo.html', {'form': form,
                                     'infos': result, 'response': response}) 


@login_required
def lastUpdated(request):
    form = StockForm()
    result=[]
    Handle = ""
    message=[]
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            Handle = form.cleaned_data['Handle'].upper()

        #checking if cached copy of historical data exists
        in_database = Historical.objects.filter(Handle = Handle).count()
        if in_database:
            temp = Historical.objects.filter(Handle = Handle).latest('Date')
            result = [temp]
        else:
            temp = SymbolInfo.objects.filter(Handle=Handle)
            if len(temp):
                temp1 = [temp] if temp.__class__ ==dict else temp
                result = [dict(Handle_id=temp[0].Handle,Date=temp[0].DateStamp)]
            else:
                message.append("Symbol %s does not exist."%Handle)
        # print result.Date
        # temp1 = [temp] if temp.__class__ ==  else temp
        # print temp1.Date

    return render(request, 'stocks/lastUpdated.html', {'form': form,
                                                 'infos': result,'message':message})

@login_required
def UpdateDatabase(request):
    form = StockForm()
    result=[]
    infos=[]
    messages =[]
    Handle=""
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            Handle = form.cleaned_data['Handle'].upper()
     
            messages= Update_database(Handle)
    return render(request, 'stocks/UpdateDatabase.html', {'form': form,
                                                 'infos': result,'messages': messages})


@login_required
def dayInfo(request):
    form = DayInfoForm()
    result=[]
    result2=[]
    if request.method == 'POST':
        form = DayInfoForm(request.POST)
        if form.is_valid():
            Date = form.cleaned_data['Date']
        result = Historical.objects.filter(Date = Date)
        result_final = [result] if result.__class__ == dict else result
        print result
        for i in result:
            temp = SymbolInfo.objects.filter(Handle = i.Handle_id)
            temp1 = [temp] if temp.__class__ == dict else temp
            a =dict(Name = temp1[0].Name , Handle_id = i.Handle_id, High = i.High, Low = i.Low)           
            result2.append(a)

    return render(request, 'stocks/dayInfo.html', {'form': form,
                                    'infos': result2})
