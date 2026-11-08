import requests

url = 'https://api.restcountries.com/countries/v5'
headers = {'Authorization': 'Bearer YOUR_KEY_HERE'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    raw_json = response.json()
else:
    print("Error, unable to fetch data from the API.")