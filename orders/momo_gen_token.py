import os 
import requests 
import uuid 
import json
import base64

class MomoService:

    def __init__(self):
        self.subscription_key = "74f9f6d2b897425092a9dbe6566714a9"
        self.base_url = "https://sandbox.momodeveloper.mtn.com"
        self.callback_host = "https://webhook.site/5a9ed3fe-dbb6-4fed-a3a6-a54bfa1d2c3d"

        self.user_id = None 
        self.api_key = None
        self.access_token = None


    
    

    # creating an momo api user 
    def create_api_user(self):
        url = f"{self.base_url}/v1_0/apiuser"
       
        # generate UUID for momo
        self.user_id = str(uuid.uuid4())

        # HEADERS
        headers = {
            'X-Reference-Id': self.user_id,
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/json", 
        }

        data = {
            "providerCallbackHost": self.callback_host,
        }


        print("sending request with headers: ", headers)
        print("sending data: ", data)

        try: 
            response = requests.post(url,headers=headers, json=data)

            print(f"Response Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Text: {response.text}")

            if response.status_code == 201:
                print("API User created successfully")
                print("User Id: ", self.user_id)
                return self.user_id
            else:
                print("Failed to create API User. Status: ", response.status_code)
                if response.status_code == 400:
                    print("Bad request - Check your data format and headers")
                elif response.status_code == 401:
                    print("Unauthorized - Check your Subscription key ")
                elif response.status_code == 409:
                    print("User already exists")

                return None
            
        except requests.exceptions.RequestException as e:
            print('Request failed: ', e)
            return None 
        

    # generate MoMo API key 
    def generate_api_key(self,user_id = None):
        
        if user_id is None:
            self.user_id = self.create_api_user()
            print(f"API User created...")
            print(f"User Id: {self.user_id}")
            

            if not self.user_id:
                print("Failed to create momo api user")
                return None
            
            return self.user_id
        
        url = f"{self.base_url}/v1_0/apiuser/{self.user_id}/apikey/"
        subscription_key = self.subscription_key

        headers = {
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/json"
        }

        try:
            print(f"Generating API key for user: {user_id}")
            response = requests.post(url, headers=headers)

            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")

            if response.status_code == 201:
                self.api_key = response.json().get("apiKey") # char "K" ii apiKey is uppercase
                print(" API Key Generated successfully")
                print(f"User Id: {self.user_id}")
                print(f"API KEY: {self.api_key}")

                # Save credentials after generating API key
                self.save_momo_credentials(self.user_id, self.api_key)

                return self.user_id, self.api_key
            else:
                print(f"Failed to generate api key: {response.status_code}")
                print(f"Error: {response.text}")
                return self.user_id, None
        
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return self.user_id, None
        
    # saving api_user and api_key in json file 
    #filepath = os.path.join('grocery_shop/orders/momo_credentials.json')
    def save_momo_credentials(self,user_id,  api_key):
        """Save credentials to JSON file"""
        # Get current directory and create proper file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(current_dir, 'momo_credentials.json')

        credentials = {
            'user_id':user_id,
            'api_key': api_key,
        }

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)


        with open(filename, "w") as f:
            json.dump(credentials, f, indent=4)

        print(f"save credentials to {filename}")


    
    def load_momo_credentials(self):
        """Load credentials from JSON file"""
        current_dir = os.path.dirname(os.path.abspath(__file__)) # **learn about this line
        filename = os.path.join(current_dir, 'momo_credentials.json')
        
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    credentials = json.load(f)
                self.user_id = credentials.get('user_id')
                self.api_key = credentials.get('api_key')
                print(f"✅ Loaded credentials for user: {self.user_id}")
                return True
            except Exception as e:
                print(f"❌ Error loading credentials: {e}")
                return False
        return False



    def generate_access_token(self):

        if not self.user_id or not self.api_key:
            if not self.load_momo_credentials():
                # If no credentials, create new ones
                print("No credentials found. Creating new API user...")
                self.user_id, self.api_key = self.generate_api_key()
                if not self.user_id or not self.api_key:
                    print("❌ Failed to create credentials")
                    return None
            
        
        url = f"{self.base_url}/collection/token/"
        subscription_key = self.subscription_key

        # basic authorization
        credentials = f"{self.user_id}:{self.api_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/json",
        }

        print("Requesting access token")
        response = requests.post(url, headers=headers)

        try:
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                token_type = response.json().get("token_type", "Bearer")
                expires_in = response.json().get("expires_in", "Unknown")

                print("✅ Access token generated successfully!")
                print(f"🔑 Token Type: {token_type}")
                print(f"⏰ Expires in: {expires_in} seconds")
                print(f"📝 Access Token: {self.access_token}")

                return self.access_token 
            else:
                print("failed to generate access token: ",response.status_code)
                print(f"Error: {response.text}")
                return None 
            
        except requests.RequestException as e:
            print(f"Request Failed {e}")
            return None
        

        
    #momo payment request
    def send_momo_payment(self, msisdn, amount, reference):

         # DEBUG: Check if we have credentials
        print(f"DEBUG - User ID: {self.user_id}")
        print(f"DEBUG - API Key: {self.api_key}")
        print(f"DEBUG - Access Token: {self.access_token}")

        url = f"{self.base_url}/collection/v1_0/requesttopay/"
        subscription_key = self.subscription_key

        self.access_token = self.generate_access_token()

        if not self.access_token:
            print("❌ Failed to generate access token")
            return 401, "Failed to generate access token" 

        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Reference-Id": reference,
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/json"
            
        }

        data = {
            "amount": str(amount),
            "currency": "EUR",
            "externalId": str(uuid.uuid4())[:8],
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": msisdn
            },
            "payerMessage": "Grocery Shop payment",
            "payeeNote": "Thank you for shopping with us."
        }

        print(f"💳 Sending payment request...")
        print(f"   To: {msisdn}")
        print(f"   Amount: {amount} EUR")  # FIXED: Currency
        print(f"   Reference: {reference}")
        print(f"   Headers: {headers}")
        print(f"   Data: {data}")


        try:
            
            response = requests.post(url, json=data, headers=headers)
            if response.status_code in [200, 202]:
                print("Payment sent successfully")
                return response.status_code, "payment request initiate"
            else:
                print("Payment failed: ", response.text)
                return response.status_code, response.text 
            
        except requests.exceptions.RequestException as e:
            print("Request failed: ", e)
            return 500, str(e)
        
        
    def check_payment_status(self, reference):
        """Check status of a payment"""
        if not self.access_token:
            self.generate_access_token()

        url = f"{self.base_url}/collection/v1_0/requesttopay/{reference}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "X-Target-Environment": "sandbox"
        }

        response = requests.get(url, headers=headers)
        return response.status_code, response.text
    

    
# Usage example
def main():
    momo = MomoService()
    
    # Test payment
    status, message = momo.send_momo_payment(
        msisdn="46733123450",  # Sandbox test number
        amount=1,
        reference=str(uuid.uuid4())
    )
    
    print(f"Final Status: {status}")
    print(f"Final Message: {message}")

if __name__ == "__main__":
    main()