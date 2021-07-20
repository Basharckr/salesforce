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
def fetch_data(parameters = {}, method = 'get', data = {}):
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s'% access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+'/services/data/v45.0/query/' , headers=headers, params=parameters, timeout=30)
        
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url + '/services/data/v45.0/query/', json=data, headers=headers, params=parameters, timeout=10)

    else:
        raise ValueError('Method should be GET or PUT or PATCH')

    if  r.status_code < 300:
        return r.json()
    else:
        raise Exception('Error when calling URL')

def hello_world(request):

    if access_token:
        dat_1 = json.dumps(fetch_data({'q': 'SELECT User.Name FROM User LIMIT 5'}), indent=2)
        dat_2 = json.dumps(fetch_data({'q': 'SELECT Account.Name FROM Account LIMIT 5'}), indent=2)
        dat_3 = json.dumps(fetch_data({'q': 'SELECT Contact.Name FROM Contact LIMIT 5'}), indent=2)
        print('users-------', dat_1)
        print('Account-----', dat_2)
        print('contacr------', dat_3)
    

    else:
        raise Exception('401 Unauthorized')

    return HttpResponse('success')



