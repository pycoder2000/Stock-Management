from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm,NewUserForm
from django.contrib import messages
import requests
import json
from .api import *
from datetime import datetime
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from finance.settings import STOCKS_API_KEY,STOCKS_API_URL
import requests
import json
from django.contrib.auth.decorators import login_required
from django import template
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm
import quandl
import pandas as pd
import numpy as np
import datetime

reg = template.Library()

api_key = 'Tpk_c46f4087296c43358402984f3b26ed2f'

@reg.filter
def split(value, arg):
    return value.split(arg)

def home(request):

    if request.method == 'GET' and  'ticker' in request.GET.keys():
        ticker = request.GET['ticker']
        api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + ticker + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
    
        # for error handling
        try:
            api = json.loads(api_request.content)
        #create an exception
        except Exception as e:
            api = "Sorry there is an error"
        return render(request, 'home.html', {'api': api} )
    else:
        return render(request, 'home.html')

@csrf_exempt
def view_stock(request):
    return render(request, 'stocks.html', {})


def register_request(request):
    if (request.method == "POST"):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def about(request):
    return render(request, 'about.html', {})

@login_required
def profile(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock ticker has been added to your Portfolio!"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.filter(user=request.user)
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
            
            # for error handling
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Sorry there is an error"
        return render(request, 'profile.html', {'ticker': ticker, 'output': output})


@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, ("Stock ticker has been added to your profile!"))
            return redirect('add_stock')
    else:

        if request.user.is_anonymous:
            ticker = []
        else:
            ticker = Stock.objects.filter(user=request.user)
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
            
            # for error handling
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Sorry there is an error"
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})
    
def list_stock_old(request):
    output = []
    if request.user.is_anonymous:
        tickerList = ''
    else:
        ticker = Stock.objects.filter(user=request.user)        
        tickerList = " ".join([t.ticker for t in ticker])
    print(tickerList)
    tickerData = GetAllStocks(tickerList)
    #tickerData = tickerData.summary_detail.update(tickerData.price)
    #print(tickerData.summary_detail)
    return render(request, 'stockList.html', {'ticker':tickerData.summary_detail|tickerData.price, 'output':output})
@login_required
def list_stock(request):
    if request.user.is_anonymous:
        ticker = []
    else:
        ticker = Stock.objects.filter(user=request.user)
    output = []
    for ticker_item in ticker:
        api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
        
        # for error handling
        try:
            api = json.loads(api_request.content)
            output.append(api)
        except Exception as e:
            api = "Sorry there is an error"
    return render(request, 'stockList.html', {'ticker': ticker, 'output': output})

@login_required
def delete(request, stock_id):
    item = Stock.objects.get(ticker=stock_id,user=request.user)
    item.delete()
    messages.success(request, ("Stock ticker has been removed from your Portfolio!"))
    return redirect(list_stock)

@login_required
def delete_stock(request):    
    ticker = Stock.objects.filter(user=request.user)
    return render(request, 'delete_stock.html', {'ticker': ticker})

def searchView(request):
    if len (request.GET['ticker']) < 1:
        return HttpResponse("")
    data = get_symbol_list(request.GET['ticker'])
    print(data)
    return render(request,'search.html',{'data':data})

def predict_home(request):
    return render(request,'predict_stock.html')

def predict(request):
    # Quandl API key. Create your own key via registering at quandl.com
    quandl.ApiConfig.api_key = "RHVBxuQQR_xxy8SPBDGV"
    # Getting input from Templates for ticker_value and number_of_days
    ticker_value = request.POST.get('ticker')
    number_of_days = request.POST.get('days')
    number_of_days = int(number_of_days)
    # Fetching ticker values from Quandl API 
    df = quandl.get("WIKI/"+ticker_value+"")
    df = df[['Adj. Close']]
    forecast_out = int(number_of_days)
    df['Prediction'] = df[['Adj. Close']].shift(-forecast_out)
    # Splitting data for Test and Train
    X = np.array(df.drop(['Prediction'],1))
    X = preprocessing.scale(X)
    X_forecast = X[-forecast_out:]
    X = X[:-forecast_out]
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.2)
    # Applying Linear Regression
    clf = LinearRegression()
    clf.fit(X_train,y_train)
    # Prediction Score
    confidence = clf.score(X_test, y_test)
    # Predicting for 'n' days stock data
    forecast_prediction = clf.predict(X_forecast)
    forecast = forecast_prediction.tolist()
    return render(request,'predict_stock.html',{'confidence' : confidence,'forecast': forecast,'ticker_value':ticker_value,'number_of_days':number_of_days})