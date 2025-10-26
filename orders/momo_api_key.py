import requests
import json
from .momo_apiuser import create_api_user



def generate_api_key(user_id=None):

    if user_id is None:
        print("creating api user...")
        user_id = create_api_user()

        if not user_id:
            print("Failed to create api user")
            return None, None 
        
    url = f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{user_id}/apikey"
    subscription_key = "74f9f6d2b897425092a9dbe6566714a9"
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"
    }

    try:
        print(f"Generating API key for user: {user_id}")
        response = requests.post(url, headers=headers)

        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        #print(type(response.json()))
        if response.status_code == 201:
            api_key = response.json().get("apiKey") # the character "K" in apiKey is uppercase
            print("✔️ API KEY Generated succesfully")
            print(f"User Id: {user_id}")
            print(f"API KEY: {api_key}")

            return user_id, api_key
        else:
            print(f"❌ Failed to generate API Key: {response.status_code}")
            print(f"Error: {response.text}")
            return user_id, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return user_id, None


def save_credentials(user_id, api_key, filename="grocery_shop/orders/momo_credentials.json"):
    momo = {}
    with open(filename, "w") as f:
        momo["user_id"] = user_id
        momo["api_key"] = api_key

        json.dump(momo, f)
        # f.write(f"User ID: {user_id}\n")
        # f.write(f"API KEY: {api_key}\n")
    print(f"save credentials to {filename}")
  

if __name__ == "__main__":
    # user_id = create_api_user()
    # generate_api_key(user_id)

    user_id, api_key = generate_api_key()
    print("\nAfter unpacking...")
    print(f"user_id: {user_id} \napi_key: {api_key}")

    if api_key:
        save_credentials(user_id,api_key)
        print("\n🎉 Success! Use these credentials for token generation:")
        print(f"User ID: {user_id}")
        print(f"API Key: {api_key}")
    else:
        print("❌ Failed to generate API key")
