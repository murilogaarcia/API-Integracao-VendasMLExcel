import requests

refresh_token = "TG-691b4b733eb95c00010d7e22-2405713476"

url = "https://api.mercadolibre.com/oauth/token"

payload = f'grant_type=refresh_token&client_id=7072255123444581&client_secret=wzOzq05aPbzdcwDMSSaJukJhiQqlI6nH&refresh_token={refresh_token}'
headers = {
  'accept': 'application/json',
  'content-type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
