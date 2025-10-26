import requests
import json
import os
import base64
from django.conf import settings
from .momo_apiuser import create_api_user
from .momo_api_key import generate_api_key

#filename = "grocery_shop/orders/momo_credentials.json"
def generate_access_token(user_id=None,api_key=None):
    """Generate access token for MTN MoMo API"""
    
    # If no credentials provided, create them
    # if user_id is None or api_key is None:
    #     print("Creating API user and generating API key...")
    #     user_id = create_api_user()
    #     if not user_id:
    #         print("❌ Failed to create API user")
    #         return None
        
    #     api_key = generate_api_key(user_id)
    #     if not api_key:
    #         print("❌ Failed to generate API key")
    #         return None

    # Use Django's BASE_DIR to create absolute path
    credentials_file = os.path.join(settings.BASE_DIR, 'orders', 'momo_credentials.json')
    #credentials_file = "grocery_shop/orders/momo_credentials.json"
    # checking whether file exist
    # if not os.path.exists(credentials_file):
    #     user_id = create_api_user()
    #     if not user_id:
    #         return None 
        
    #     api_key = generate_api_key()
    #     if not api_key:
    #         return None 
        
    #     #create directory if doesn't exist
    #     os.makedirs(os.path.dirname(momo_credentials), exist_ok=True)

    #     #save credentials 
    #     momo_credentials = {
    #         "user_id": user_id,
    #         "api_key": api_key
    #     }

    #load credential
    try:
        with open(credentials_file) as f:
            momo_credentials = json.load(f)

        user_id = momo_credentials.get('user_id')
        api_key = momo_credentials.get('api_key')

        if not user_id or not api_key:
            raise ValueError("Invalid credentials in file")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error reading credentials: {e}")
        
        return generate_access_token()

    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    subscription_key = "74f9f6d2b897425092a9dbe6566714a9"  # Fixed typo: subcription -> subscription

    # Basic auth header
    credentials = f"{user_id}:{api_key}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"  # FIXED: Changed from "Content-Key"
    }

    print(f"Requesting access token for user: {user_id}")
    print(f"Using API Key: {api_key[:10]}...")  # Show first 10 chars for security

    try:
        response = requests.post(url, headers=headers)
        
        print(f"Token Response Status: {response.status_code}")
        print(f"Token Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            token_type = response.json().get("token_type", "Bearer")
            expires_in = response.json().get("expires_in", "Unknown")
            
            print("✅ Access token generated successfully!")
            print(f"🔑 Token Type: {token_type}")
            print(f"⏰ Expires in: {expires_in} seconds")
            print(f"📝 Access Token: {access_token}")
            
            return access_token
        else:
            print(f"❌ Failed to generate access token: {response.status_code}")
            print(f"Error details: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

# Alternative function using existing credentials
# def generate_access_token_with_credentials(user_id, api_key):
#     """Generate access token using existing credentials"""
#     url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
#     subscription_key = "74f9f6d2b897425092a9dbe6566714a9"

#     credentials = f"{user_id}:{api_key}"
#     encoded_credentials = base64.b64encode(credentials.encode()).decode()

#     headers = {
#         "Authorization": f"Basic {encoded_credentials}",
#         "Ocp-Apim-Subscription-Key": subscription_key,
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, headers=headers)
    
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Token generation failed: {response.status_code} - {response.text}")
#         return None

if __name__ == "__main__":
    print("=== MTN MoMo Access Token Generator ===")
    
    # Option 1: Generate new credentials and token
    token = generate_access_token()
    
    # Option 2: Use existing credentials
    # user_id = "YOUR_EXISTING_USER_ID"
    # api_key = "YOUR_EXISTING_API_KEY"
    # token = generate_access_token(user_id, api_key)
    
    if token:
        print(f"\n🎉 Success! Use this token in your requests:")
        print(f"Authorization: Bearer {token}")
    else:
        print("\n❌ Failed to generate access token")    
