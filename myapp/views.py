from django.shortcuts import render
import requests
from django.http import HttpResponse
import json
from decouple import config

# Create your views here.


params = {
    "grant_type":"password",
    "client_id":config('client_id'),
    "client_secret":config('client_secret'),
    "username":"bashar@ckr.com",
    "password":config('password')
}
r = requests.post("https://login.salesforce.com/services/oauth2/token",params=params)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")

def fetch_data(action, parameters = {}, method = 'get', data = {}):
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s'% access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url, headers=headers, params=parameters, timeout=30)
        print('onlyyyy r', r)
        print('jsonnnnnnnnn r', r.json())
        
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url + action, json=data, headers=headers, params=parameters, timeout=10)

    else:
        raise ValueError('Method should be GET')

    if  r.status_code < 300:
        return r.json()
    else:
        raise Exception('Error when calling URL')

def hello_world(request):

    if access_token:
        dat = json.dumps(fetch_data('/services/data/v45.0/query/', {'q': 'SELECT Account.Name, Name, CloseDate from Accounts where IsClose = True'}), indent=2)
    else:
        print("nooppp")

    return HttpResponse(dat)



