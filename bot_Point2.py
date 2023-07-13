from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time as time
import csv                                                                                                                                                                                                            # Replace 'path_to_webdriver' with the path to your downloaded web driver
driver = webdriver.Chrome(r"C:\Users\Kenzo Noguera\Desktop\Gadgets\chromedriver_win32\chromedriver.exe")
driver.implicitly_wait(10)

# Load the webpage
driver.get('https://pro.point2homes.com/Listings/AddListing')
time.sleep(5)

def login_password():
    # Input text in the "UserName" field
    username_element = driver.find_element(By.ID, 'Username')
    username_element.send_keys(r'toddcutter')

    # Input text in the "Password" field
    password_element = driver.find_element(By.ID, 'Password')
    password_element.send_keys(r"Np2hxh725!@?")

    #input("Press Enter to exit...")

    # Find and click the submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()

login_password()

# Wait for a few seconds (adjust the timeout value as needed)
time.sleep(5)

# Load the CSV file
with open(r"C:\Users\Kenzo Noguera\Desktop\APP PROJECT\Code\Selenium_Version\Curridabat Torres de Granadilla\Curridabat Torres de Granadilla_MLS_Data.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        attribute_id = row['ATTRIBUTE']
        attribute_value = row['VALUE']
        
        # Find the elements with the attribute ID 'Description' and class 'form-control'
        elements = driver.find_elements(By.CSS_SELECTOR, f'#{attribute_id}.form-control')
        
        # Input text from CSV to each matching element
        for element in elements:
            element.send_keys(attribute_value)
            time.sleep(3)
    input("Press Enter to exit...")
        
