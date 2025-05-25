import requests
from bs4 import BeautifulSoup
import webbrowser

def web_scraper(url):
    # Send a request to the website
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract and print all the headings 
    print("\nHeadings found on the page:")
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        print(heading.get_text(strip=True))
    
    # Extract and print all the links (anchor tags)
    print("\nLinks found on the page:")
    links = soup.find_all('a', href=True)
    for i, link in enumerate(links):
        text = link.get_text(strip=True) or "No text"
        print(f"{i + 1}. {text} → {link['href']}")

    # Ask user to open a link
    try:
        choice = int(input("\nEnter the number of the link to open in a new window (0 to skip): "))
        if 1 <= choice <= len(links):
            selected_link = links[choice - 1]['href']
            if not selected_link.startswith('http'):
                selected_link = requests.compat.urljoin(url, selected_link)
            webbrowser.open_new(selected_link)  # Open in a new browser window
            print(f"Opened: {selected_link}")
        else:
            print("No link opened.")
    except ValueError:
        print("Invalid input.")

url = input("Enter the URL of the website you want to scrape: ")
web_scraper(url)
