import requests 
import json 
from django.conf import settings 


def checkout(payload):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        'https://api.paystack.co/transaction/initialize',
        headers=headers, 
        data=json.dumps(payload)
    )
    response_data = response.json() 

    if response_data.get('status') == True:
        return True, response_data['data']['authorization_url']
    else:
        return False, "Failed to initiate payment, please try again later." 
    

def verify_payment(reference):
    """verify paystackt payment and return status, verification_data"""

    try:
        headers = {
            "Authorization":f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "applicaiton/json"
        }

        response = requests.get(
            f"https://api.paystack.co/transaction/verify/{reference}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            return data['status'], data['data']
        else:
            return False, None
        
    except Exception as e:
        return False, None 
    
    