import requests

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

url = "https://api.producthunt.com/v2/oauth/token"
client_id='MTSirDr2G9cjl4JQHFW09YYYvyoh4SaxH4qFJIx1Lsc'
client_secret='_BMbEwqr-sT-8j4D2SuHyysA3YhXU2TaHuD2kGUjzeI'
data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}
access_token = 'GP8apsXTdNnxqgxKDlK9NMGBZ5tL0pgIGqDDYzIJ1ug'
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}


# response = requests.post(url, json=data)
# token = response.json()["access_token"]
# print("✅ Access token:", token)

