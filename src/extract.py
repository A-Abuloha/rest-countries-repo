import requests
import json

def extract_data():
    base_url = 'https://api.restcountries.com/countries/v5'
    headers = {'Authorization': 'Bearer YOUR_KEY_HERE'}
    
    all_countries = []
    offset = 0
    more_data = True
    
    print("Fetching data from API (handling pagination)...")
    
    # Loop to request new pages until 'more' is False
    while more_data:
        url = f"{base_url}?offset={offset}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract countries from the current page and add to our master list
            objects = data.get('data', {}).get('objects', [])
            all_countries.extend(objects)
            
            # Check the meta block to see if we need to keep looping
            meta = data.get('data', {}).get('meta', {})
            more_data = meta.get('more', False)
            limit = meta.get('limit', 25)
            
            print(f"Fetched {len(objects)} countries... (Total downloaded so far: {len(all_countries)})")
            
            # Increase the offset by 25 to grab the next page on the next loop
            offset += limit
        else:
            print(f"Error fetching data. Status code: {response.status_code}")
            break
            
    # Re-pack all 254 countries into the original JSON structure
    final_json = {"data": {"objects": all_countries}}
    
    with open('data/raw/rest_countries_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
        
    print("All data successfully saved to data/raw/rest_countries_data.json!")

if __name__ == "__main__":
    extract_data()