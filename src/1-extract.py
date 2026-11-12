import requests
import json

def extract_data():
    url = 'https://api.restcountries.com/countries/v5'
    headers = {'Authorization': 'hi'}  # Replace with your actual API token

    all_countries = []
    offset = 0
    has_more = True
    
    print("Fetching data from API (handling pagination)...")
    
    # Loop to request new pages until 'more' is False
    while has_more:
        params = {'offset': offset}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract countries from the current page and add to our master list
            objects = data.get('data', {}).get('objects', [])
            all_countries.extend(objects)
            
            # Check the meta block to see if we need to keep looping
            meta = data.get('data', {}).get('meta', {})
            has_more = meta.get('more', False)
            count = meta.get('count', 0)
            
            print(f"Fetched {count} countries... (Total downloaded so far: {len(all_countries)})")
            
            # Increase the offset by 25 to grab the next page on the next loop
            offset += count
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