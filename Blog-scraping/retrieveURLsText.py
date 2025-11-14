import requests
from bs4 import BeautifulSoup

def fetch_text_from_url(url):
    # Add https scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract all text from the body of the HTML
        body_text = soup.body.get_text(separator='\n', strip=True)
        return body_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_text_to_file(title, url_file):
    # Create or open a text file for writing
    txt_filename = title.replace(" ", "_") + ".txt"
    
    with open(txt_filename, 'w', encoding='utf-8') as file:
        # Write the title at the top of the file
        file.write(f"{title}\n")
        file.write("=" * len(title) + "\n\n")
        
        # Read URLs from file
        with open(url_file, 'r') as urls:
            for url in urls:
                url = url.strip()
                if url:
                    print(f"Fetching text from {url}")
                    text = fetch_text_from_url(url)
                    if text:
                        file.write(f"URL: {url}\n")
                        file.write(text + "\n\n")
                    else:
                        file.write(f"Failed to retrieve content from {url}\n\n")
    
    print(f"Text saved to {txt_filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <Document Title> <URL File>")
    else:
        document_title = sys.argv[1]
        url_file = sys.argv[2]
        save_text_to_file(document_title, url_file)
