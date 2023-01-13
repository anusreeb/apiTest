from django.shortcuts import render
from django.http import HttpResponse
import requests
import pandas as pd
import json
import time
from datetime import datetime

MAX_RETRIES = 5

# Create your views here.
def transactions(request):
    if not request.GET.get('merchant_id'):
        return HttpResponse("please provide merchant_id as query param")
    if not request.GET.get('date'):
        return HttpResponse("please provide date as query param")
    merchant_id = request.GET.get('merchant_id')
    date = request.GET.get('date')
    num_retries = 0
    while num_retries<MAX_RETRIES:
        response = requests.get('https://api-engine-dev.clerq.io/tech_assessment/transactions/?merchant=' + merchant_id)
        if response.status_code == 200:
            #Get transactions in json
            transactions_json = response.json()
            #Create dataframe from transactions json
            df = pd.DataFrame(transactions_json['results'])
            #turning strings to floats
            df = df.astype({"amount": float})
            #making sure there are no negative numbers
            df['amount'] = df['amount'].abs()
            df['just_date'] = df['updated_at'].astype('datetime64[ns]').dt.date
            #filtering only transactions for that date
            print(datetime.strptime(date, '%Y-%m-%d').date())
            df = df[df['just_date']==datetime.strptime(date, '%Y-%m-%d').date()]
            refunds = df[df['type']=='REFUND']
            sales = df[df['type']=='SALE']
            net_amount = sales['amount'].sum()-refunds['amount'].sum()
            settlement_result = {"merchant_id":merchant_id,"date":date,"net_settlement_amount":net_amount}
            return HttpResponse(json.dumps(settlement_result), content_type="application/json")
        else:
            num_retries +=1
            time.sleep(5)
    return HttpResponse('Something went wrong',status=response.status_code)
    pass

