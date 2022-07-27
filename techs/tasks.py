from phone_wholesale.celery import app
import requests
from celery import shared_task
from .models import Phone

@shared_task
def gsx_api_update(phone_id, PARAMS, URL):
    phone = Phone.objects.get(id=phone_id)
    print(phone.imei)
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    if data['flag'] == 'ok':
        if 'OFF' in data['result']:
            print('Unlock')
            phone.is_locked='UN'
            phone.save()
        else:
            print('locked')
            phone.is_locked='LO'
            phone.save()
    elif data['flag'] == 'fail':
        print('failed')
        phone.is_locked='FA'
        phone.save()
    else:
        print('API Call Failed')