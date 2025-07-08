import requests

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

url = "https://api.producthunt.com/v2/oauth/token"

data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}


# response = requests.post(url, json=data)
# token = response.json()["access_token"]
# print("✅ Access token:", token)

