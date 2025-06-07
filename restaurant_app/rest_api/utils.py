from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.conf import settings
from base64 import b64encode
import requests
import traceback

RED = "\033[31m"
RESET = "\033[0m"


def custom_exception_handler(exc, context):
    if settings.DEBUG == True:
        print(f"{RED}####### WARNING! CRITICAL ERROR! ######{RESET}\n")
        print(f"{RED}Context:{RESET} {context}\n{RED}Error:{RESET} {exc}\n")
        print(f"{RED}Traceback (most recent call last):{RESET}")
        print(traceback.format_exc())
        print(f"{RED}#######################################{RESET}\n")

    response = exception_handler(exc, context)
    if response is None:
        return Response({"error": "An unexpected error occurred"}, status=500)
    return response



def get_oauth_token():        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(
            settings.PAYU_OAUTH_URL,
            headers=headers,
            data={
                'grant_type': 'client_credentials',
                'client_id':settings.PAYU_CLIENT_ID, 
                'client_secret': settings.PAYU_CLIENT_SECRET }
        )
        if response.status_code != 200:
            raise Exception('Failed to obtain PayU OAuth token')
            
        return response.json()['access_token']


def get_payu_order_status(payu_order_id, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{settings.PAYU_API_URL}/orders/{payu_order_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    return None
