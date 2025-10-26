import requests
import uuid 

def create_api_user():
    url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"
    subscription_key = "74f9f6d2b897425092a9dbe6566714a9"
    callback_host = "https://webhook.site/5a9ed3fe-dbb6-4fed-a3a6-a54bfa1d2c3d"

    # Generate UUID for momo
    user_id = str(uuid.uuid4())
    print(f"user_id: {user_id}")

    # CORRECTED HEADERS - Fixed Content-Type typo
    headers = {
        "X-Reference-Id": user_id,
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json",  # FIXED: Changed underscore to hyphen
    }

    data = {
        "providerCallbackHost": callback_host,  # Note: "Callback" not "CallBack"
    }

    print("Sending request with headers:", headers)
    print("Sending data:", data)

    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 201:  # MTN typically returns 201 for success
            print("✅ API User created successfully!")
            print("User ID:", user_id)
            return user_id
        else:
            print(f"❌ Failed to create API User. Status: {response.status_code}")
            if response.status_code == 400:
                print("Bad Request - Check your data format and headers")
            elif response.status_code == 401:
                print("Unauthorized - Check your subscription key")
            elif response.status_code == 409:
                print("User already exists")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    create_api_user()