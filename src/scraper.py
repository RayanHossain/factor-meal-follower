from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def fetch_delivery_status(url):
    """
    Fetches the delivery status from the meal delivery service's tracking page using Selenium.
    
    Args:
        url (str): The URL of the delivery tracking page.
    
    Returns:
        dict: A dictionary containing the delivery status, image URL, or an error message.
    """

    # Set up the Selenium WebDriver
    driver = webdriver.Firefox()
    

    delivery_info = {
        'status': None,
        'image_url': None,
        'error': None
    }

    driver.get(url)  # Load the website
    time.sleep(1)

    try:
        # Check if delviery is still in progress
        expected_delievery_element = driver.find_elements(By.CSS_SELECTOR, 'div.plannedDate')
        if expected_delievery_element:
            # Update delivery information
            delivery_info['status'] = f"Expected delivery time is: {expected_delievery_element.text}"  
            delivery_info['image_url'] = None 

            return delivery_info

        # Check if delivery completed, obtaining both the time at which it is delivered and an image of the delivery
        delivered_elements = driver.find_elements(By.CSS_SELECTOR, 'div.deliveredPhase')

        if delivered_elements:
            delivered_image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.frontDoorPictureContainer img')

            if delivered_image_elements:
                delivery_info['status'] = delivered_elements[0].text  # Delivery completed status
                delivery_info['image_url'] = delivered_image_elements[0].get_attribute('src')  # Image URL

            else:
                delivery_info['status'] = delivered_elements[0].text
                delivery_info['image_url'] = None  # No image available
        
        # Check if the website is no longer tracking this order.
        not_in_use_elements = driver.find_elements(By.CSS_SELECTOR, 'div.invalidLink div.bottomText')
        if not_in_use_elements:
            delivery_info['status'] = not_in_use_elements[0].text

        return delivery_info
        
    
    except (NoSuchElementException, TimeoutException):
        delivery_info['error'] = "No delivery status found on the page."

    except Exception as e:
        delivery_info['error'] = f"An unexpected error occurred: {e}"
        
    finally:
        driver.quit()  # Close the WebDriver after use

    return delivery_info

def fetch_multiple_delivery_statuses(urls):
    results = {}
    for url in urls:
        status = fetch_delivery_status(url)
        results[url] = status
    return results

if __name__ == "__main__":
    tracking_urls = ["https://status.factormeals.ca/6172d06257", # past order
                     "https://status.factormeals.ca/7cb6edc5fb", # works too and is upcoming
                    ]

    #status = fetch_multiple_delivery_statuses(tracking_urls)
    upcoming_delivery = "https://status.factormeals.ca/7cb6edc5fb"
    past_delivery = "https://status.factormeals.ca/6172d06257"

    #delivery_status = fetch_delivery_status(url = past_delivery)
    
    orders = fetch_multiple_delivery_statuses(tracking_urls)

    print(orders)
