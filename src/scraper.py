import requests
from bs4 import BeautifulSoup
import logging
import os
import re

# Set up the logging file
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging to write to a file with a specific format
logging.basicConfig(
    filename='logs/scraper.log',  # Log file path
    level=logging.INFO,           # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format with timestamps
    datefmt='%Y-%m-%d %H:%M:%S'   # Date and time format
)

def fetch_delivery_status(url):
    """
    Fetches the delivery status from the meal delivery service's tracking page.
    
    Args:
        url (str): The URL of the delivery tracking page.

    Returns:
        str: The extracted delivery status or an error message.
    """

    logging.info(f"Fetching delivery status for URL: {url}")
    try:
        # Send an HTTP request to the delivery tracking page
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())  # Print the parsed HTML structure


        # Extract the delivery status 
        delivery_status = soup.find('div', class_= re.compile('deliveredPhase'))  # Adjust this selector based on the actual HTML
        
        if delivery_status:
            logging.info(f"Successfully fetched delivery status: {delivery_status}")
            return status.text.strip()
        else:
            logging.warning(f"No delivery status found on the page for {url}")
            return "Status not found"
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching delivery status for {url}: {e}")
        print(f"Error fetching the delivery status: {e}")
        return None

def fetch_multiple_delivery_statuses(urls):
    results = {}
    for url in urls:
        status = fetch_delivery_status(url)
        results[url] = status
    return results

if __name__ == "__main__":
    tracking_urls = ["https://status.factormeals.ca/20d758b57",
                     "https://status.factormeals.ca/14ebf053e8", # this one works
                     "https://status.factormeals.ca/4d6d0dd6a2"]
    

    #status = fetch_multiple_delivery_statuses(tracking_urls)
    status = fetch_delivery_status(url="https://status.factormeals.ca/14ebf053e8")
    print(f"Delivery status: {status}")
