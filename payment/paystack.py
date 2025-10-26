from django.conf import settings 
import requests
import uuid


class Paystack:
    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY 
    base_url = "https://api.paystack.co/"

    def verify_payment(self,reference, *args, **kwargs):
        path = f"transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SK}",
            'Content-Type': 'application/json'
        }

        url = self.base_url + path 
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("verify payment")
            response_data = response.json()
            #print(f"Response data status: {response_data['status']}")
            print(f"response data: {response_data['data']}")
            return response_data['status'], response_data['data']

        response_data = response.json()
        return response_data['status'], response_data['message']