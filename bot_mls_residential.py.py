from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time as time
import csv   
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains


def go_to_next_page(driver, page_name):
        next_button = driver.find_element(By.NAME, 'form.buttons.next')
        next_button.click()
        print(str(page_name) + " Page Completed")
def get_elements_and_input_them(driver,page_name,data):
        visible_elements = get_visible_element_names(driver)
        #print('visible elements---------->')
        #print(visible_elements)
        elements_on_csv = [row['ATTRIBUTE'] for row in data if row['ATTRIBUTE'] in visible_elements]
        #print('Elements Available--------->')
        #print(elements_on_csv)
        if len(elements_on_csv) == 0:
             go_to_next_page(driver, page_name)
        else:
            to_be_sent = [row for row in data if row['ATTRIBUTE'] in elements_on_csv]
            #print('Info to be sent------------->')
            #print(to_be_sent)
            input_data(driver, to_be_sent)
            go_to_next_page(driver, page_name)

        #if not data_inputted:
            #print("No data inputted")
            #print("NEXT CLICKED")
            #continue  # Continue the loop if no data is inputted

def login_page(driver):
    # Load the webpage
    driver.get(r'https://mls.re.cr/agencies/2cr/listings/add_residential_sale')
    wait = WebDriverWait(driver, 1)

    # Input text in the "UserName" field
    username_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, 'login')))
    username_element.send_keys('todd@2costaricarealestate.com')
    # Input text in the "Password" field
    password_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, 'password')))
    password_element.send_keys('Toooooodd2021?')

    submit_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, 'buttons.login')))
    submit_button.click()

    # Wait for a few seconds (adjust the timeout value as needed)
    wait = WebDriverWait(driver,1)

def classic_input(driver, t_attribute, t_value):
    # Find the radio button input by attribute and value
    text_input = driver.find_element(By.NAME ,t_attribute)
    
    # Move to the text element to ensure it is in view
    ActionChains(driver).move_to_element(text_input).perform()

    # Click the span element
    text_input.send_keys(t_value)
    
def date_input(driver,d_attribute,d_value):
    # Find the radio button input by attribute and value
    text_input = driver.find_element(By.CSS_SELECTOR, f'input[name="{d_attribute}"]')
    
    # Move to the text element to ensure it is in view
    ActionChains(driver).move_to_element(text_input).perform()

    # Click the span element
    text_input.send_keys(t_value)
    pyautogui.press('enter')

def multiple_options_input(driver, b_attribute, b_value):
    # Find the radio button input by attribute and value
    radio_input = driver.find_element(By.CSS_SELECTOR, f'input[name="{b_attribute}"][value="{b_value}"]')
    
    # Find the label element associated with the radio button
    label_element = driver.find_element(By.CSS_SELECTOR, f'label[for="{radio_input.get_attribute("id")}"]')

    # Move to the label element to ensure it is in view
    ActionChains(driver).move_to_element(label_element).perform()
    
    # Wait until the span element with the desired value is clickable
    wait = WebDriverWait(driver, 1)
    span_element =  label_element.find_element(By.TAG_NAME, 'span')

    # Scroll to the label element
    #driver.execute_script("arguments[0].scrollIntoView(true);", span_element)

    # Move to the label element to ensure it is in view
    ActionChains(driver).move_to_element(span_element).perform()
    
    # Click the span element
    span_element.click()


def bool_input(driver, bool_attribute, bool_value):

    # Find the radio button input by attribute and value
    radio_input = driver.find_element(By.CSS_SELECTOR, f'input[name="{bool_attribute}"][value="{bool_value}"]')


    # Find the label element associated with the radio button
    label_element = driver.find_element(By.CSS_SELECTOR, f'label[for="{radio_input.get_attribute("id")}"]')

    # Move to the label element to ensure it is in view
    ActionChains(driver).move_to_element(label_element).perform()
    
    # Wait until the span element with the desired value is clickable
    wait = WebDriverWait(driver, 1)
    span_element =  label_element.find_element(By.TAG_NAME, 'span')

    # Move to the label element to ensure it is in view
    ActionChains(driver).move_to_element(span_element).perform()
    
    # Click the span element
    span_element.click()

#def combobox_input():

def get_visible_element_names(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.span9 *')
    visible_element_names = []
    for element in elements:
        if element.is_displayed():
            name = element.get_attribute('name')
            if name:
                visible_element_names.append(name)
    #print("Visible Elements:", visible_element_names)
    return visible_element_names

def input_data(driver, data):
    data_inputted = False  # Flag to check if any data is inputted
    for row in data:
        attribute_id = row['ATTRIBUTE']
        attribute_value = row['VALUE']
        value_type = row['VALUE_TYPE']
        element = driver.find_element(By.NAME, attribute_id)
        if value_type == 'CLASSIC':
            try:
                classic_input(driver,attribute_id,attribute_value)
            except NoSuchElementException:
                print('Error inputing' + str(attribute_value))
        elif value_type == 'DATE':
            try:
                date_input(driver,d_attribute,d_value)
            except NoSuchElementException:
                print('Error inputing' + str(attribute_value))
        elif value_type == 'MULTIPLE_CHOICE' :
            try:
                multiple_options_input(driver,attribute_id,attribute_value)
            except NoSuchElementException:
                print('Error inputing' + str(attribute_value))
        elif value_type == 'BOOLEAN_CHOICE':
            if attribute_value == 'FALSE':
                attribute_value = 'false'
            elif attribute_value == 'TRUE':
                attribute_value = 'true'
            try:
                bool_input(driver, attribute_id, attribute_value)
            except NoSuchElementException:
                print('Error inputing' + str(attribute_value))

    return data_inputted

def main():
    driver = webdriver.Chrome(r"C:\Users\Kenzo Noguera\Desktop\Gadgets\chromedriver_win32\chromedriver.exe")
    # Read the CSV file and store the data in a list of dictionaries
    loged_in = False
    if loged_in == False:
        login_page(driver)
        loged_in = True
    pages = ['Basic Info','Geography','Details','Features','Infrastructure','Financial/Legal','Agent','Owner']
    which_page_are_we_in = 0
    data = []
    with open(r"C:\Users\Kenzo Noguera\Desktop\APP PROJECT\Code\Selenium_Version\Curridabat Torres de Granadilla\Curridabat Torres de Granadilla_MLS_Data.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
        #print('Data---------->')
        #print(data)
    while which_page_are_we_in < 7:
        get_elements_and_input_them(driver,pages[which_page_are_we_in],data)
        which_page_are_we_in = which_page_are_we_in + 1
    input("Press Enter to exit...")
if __name__ == '__main__':
    main()
