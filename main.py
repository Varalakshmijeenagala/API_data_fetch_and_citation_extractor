import requests
import re
import json
import string

# Constants
API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"
PAGE_SIZE = 10  # Adjust as needed for the API

#Fetches the Data from API
def fetch_data(api_url, page_size):
    data = []
    page = 1
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(api_url, params={'page': page, 'size': page_size})
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            break
        try:
            json_response = response.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            break
        
        if not isinstance(json_response, dict) or 'data' not in json_response or 'data' not in json_response['data']:
            print("Error: Expected a list of objects from API")
            print("Raw response:", json.dumps(json_response, indent=4))
            break
        
        page_data = json_response['data']['data']
        if not isinstance(page_data, list):
            print("Error: Expected a list of objects in 'data' field")
            print("Raw response:", json.dumps(json_response, indent=4))
            break
        
        if not page_data:
            break
        
        data.extend(page_data)
        
        # Check if there's a next page
        if not json_response['data'].get('next_page_url'):
            break
        page += 1
    
    return data

def normalize_text(text):
    """Normalize text by removing punctuation and converting to lower case."""
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

def get_response_sources(response_text, sources):
    citations = []
    for source in sources:
        context = source.get('context', '')
        if isinstance(context, str):
            if source.get('link','') and source['id']:
                citations.append({
                    "id": source['id'],
                    "link": source.get('link', '')
                })
    return citations

def main():
    data = fetch_data(API_URL, PAGE_SIZE)
    if not data:
        print("No data fetched from the API.")
        return

    results = []

    for item in data:
        if not isinstance(item, dict):
            print(f"Skipping invalid item: {item}")
            continue

        response_text = item.get('response')
        sources = item.get('source', [])
        if not response_text or not isinstance(sources, list):
            print(f"Skipping item with invalid response or sources: {item}")
            continue

        citations = get_response_sources(response_text, sources)
        results.append({
            "response": response_text,
            "citations": citations
        })
    #Output will be written to a json file
    with open('citations_output.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("Citations have been saved to citations_output.json")

if __name__ == "__main__":
    main()
