import requests, uuid
from .momo_api_token import generate_access_token

def send_momo_payment(msisdn,amount,reference):
    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"

    token = generate_access_token()

    print(f"\ntoken: {token}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Reference-Id": reference,
        "X-Target-Environmnet": "sandbox",
        "Ocp-Apim-Subscription-Key": "74f9f6d2b897425092a9dbe6566714a9",
        "Content-Type": "Application/json"

    }

    data = {
        "amount":str(amount),
        "currency": "GHS",
        "externalId": "1234567",
        "payer": {"partyIdType": "MSISDN",\
                   "partyId": msisdn},
        "payermessage":"Grocery Shop payment",
        "payeeNote": "Thank you for shopping with us."
    }

    r = requests.post(url, json=data, headers=headers)
    return r.status_code, r.text 
