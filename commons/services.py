import requests
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import json

def sms(message, to):
    link = 'http://37.130.202.188/api/select'
    json1 = {
        "op" : "send",
        "uname" : "farzadkaramouz",
        "pass":  "13641030",
        "message" : message, # "سلام",
        "from": "100020400",
        "to" : to, # ["09128048897"],
        "time" : ""    #//If you want to send in the future  ==> $time = '2016-07-30'
    }
    r = requests.post(link, data = json.dumps(json1))
    return print(r)
# from zarrinpal.views import sms

def sms_130(message, to):
    link = 'http://37.130.202.188/api/select'
    json1 = {
        "op": "pattern",
        "user": "farzadkaramouz",
        "pass": "13641030",
        "fromNum": "100020400",
        "toNum": to,
        "patternCode": "130",
        "inputData" :  message
    }
    print(message)
    print(to)
    r = requests.post(link, data = json.dumps(json1, cls=DjangoJSONEncoder))
    return print(r)

def sms_384(input_data, to):
    link = 'http://37.130.202.188/api/select'
    json1 = {
        "op": "pattern",
        "user": "farzadkaramouz",
        "pass": "13641030",
        "fromNum": "100020400",
        "toNum": to,
        "patternCode": "384",
        "inputData" :  input_data
    }
    # print(json1)
    # print(json.dumps(json1))
    r = requests.post(link, data = json.dumps(json1))
    return r




    