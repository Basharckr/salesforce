from django.shortcuts import render
import requests
from django.http import HttpResponse
import json

# Create your views here.


params = {
    "grant_type":"password",
    "client_id":"3MVG9fe4g9fhX0E7mOXRFi99O5F3.HzSAIP2C7Gn.c6qy7nP6yMcpCSVhwlEh_XA3NX9vn3CAYUwhnmPtR_Zf",
    "client_secret":"7A858C616773D1975781E3BDE350AE01D1FBD3EB1CE6A0D6FE462FE48CF0BF25",
    "username":"bashar@ckr.com",
    "password":"salesforce@123XX5BvlxisDpM68H5RS7lYqVr"
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



