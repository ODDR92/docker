import requests
import pandas as pd
from newspaper import Article

def search_web(query, api_key, cse_id, **kwargs):
    # Make a request to the Google Custom Search JSON API
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
    }
    params.update(kwargs)  # Add any additional parameters
    response = requests.get(url, params=params)
    response.raise_for_status()  # Ensure we got a successful response

    # Parse the JSON response
    result = response.json()

    # Extract the URLs from the search results
    urls = [item['link'] for item in result['items']]
    return urls

def extract_content(url):
    # Use newspaper3k to download and parse the article
    article = Article(url)
    article.download()
    article.parse()

    # Extract the title and text
    title = article.title
    content = article.text

    return title, content

def main():
    # Define your API key and custom search engine ID
    api_key = "AIzaSyDeQ231pa4yAlbe6X_FniwAGDCEPvbqnvA"  # Be sure to keep this secret!
    cse_id = "b11a5e75449914b36"  # Replace with your Custom Search Engine ID

    # Search the web for relevant pages
    urls = search_web("Surge esports agency", api_key, cse_id)

    data = []
    for url in urls:
        try:
            title, content = extract_content(url)
            data.append({'Title': title, 'Content': ''})  # Add title as a separate row
            data.append({'Title': '', 'Content': content})  # Add content as a separate row
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            continue  # Skip to the next URL

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    # Save data to a CSV file
    df.to_csv('surge.csv', index=False)

if __name__ == '__main__':
    main()
