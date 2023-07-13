from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time as time
import csv   
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException, StaleElementReferenceException
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

def go_to_next_page(driver,page_number):
    page_names = ['Generales','Basicos','Caracteristicas','Publicidad']
    page_ids = ['navBasicos','navCaracteristicas','navPublicidad']
    if page_number < 3:
        page_click =  driver.find_element(By.CSS_SELECTOR, "a#{}".format(page_ids[page_number]))
        driver.implicitly_wait(2)
        page_click.click()
        print(page_names[page_number] + '' + 'page completed')
        driver.implicitly_wait(50)

def get_visible_element_ids(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, '*')
    visible_element_ids = []
    for element in elements:
            if element.is_displayed():
                id_ = element.get_attribute('id')
                if id_:
                    visible_element_ids.append(id_)
        #print("Visible Elements:", visible_element_names)
    return visible_element_ids

def save_draft(driver):
    try:
        save_button = driver.find_element(By.ID,"liSave")
        ActionChains(driver).move_to_element(save_button).perform()
        save_button.click()
        save_button.click()
        driver.implicitly_wait(10)
    except ElementNotInteractableException:
        save_button = driver.find_element(By.ID,"liSaveEdit")
        ActionChains(driver).move_to_element(save_button).perform()
        save_button.click()
        save_button.click()
        driver.implicitly_wait(10)

def get_elements_and_input_them(driver,page_number,data):  
    visible_elements = get_visible_element_ids(driver)
    #print('visible elements---------->')
    #print(visible_elements)
    elements_on_csv = [row['ATTRIBUTE'] for row in data if row['ATTRIBUTE'] in visible_elements]
    #print('Elements Available--------->')
    #print(elements_on_csv)
    if len(elements_on_csv) == 0:
         go_to_next_page(driver,page_number)
    else:
        to_be_sent = [row for row in data if row['ATTRIBUTE'] in elements_on_csv]
        #print('Info to be sent------------->')
        #print(to_be_sent)
        input_data(driver, to_be_sent)
        go_to_next_page(driver,page_number)

    #if not data_inputted:
        #print("No data inputted")
        #print("NEXT CLICKED")
        #continue  # Continue the loop if no data is inputted

def login_page(driver):
    # Replace 'path_to_webdriver' with the path to your downloaded web driver
    driver.implicitly_wait(10)

    # Load the webpage
    driver.get('https://mx.omnimls.com/propiedades/agregar')
    driver.implicitly_wait(1)

    # Input text in the "UserName" field
    username_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.form-control.form-control-solid.h-auto.p-6.rounded-lg[name="_username"]')))
    username_element.send_keys('todd@2costaricarealestate.com')

    # Input text in the "Password" field
    password_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.form-control.form-control-solid.h-auto.p-6.rounded-lg[name="_password"]')))
    password_element.send_keys('Luxury2023#!')

    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'kt_login_signin_submit')))
    submit_button.click()
    driver.implicitly_wait(1)

def create_draft(driver):
    Place_Input = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-selection__rendered[id="select2-busquedaDireccion-container"]')))
    Place_Input.click()
    driver.implicitly_wait(5)
    pyautogui.write('Escazu')
    time.sleep(2)
    pyautogui.press('Enter')
    time.sleep(1)
    pyautogui.press('tab',presses = 10)
    pyautogui.press('Enter')
    time.sleep(4)
    save_draft(driver)

def classic_input(driver, t_attribute, t_value):
    # Find the radio button input by attribute and value
    text_input = driver.find_element(By.ID ,t_attribute)
    
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

def multiple_options_input(driver, b_attribute, b_value):
    el = driver.find_element(By.ID,b_attribute)
    for option in el.find_elements(By.TAG_NAME,'option'):
        if option.text == b_value:
            option.click() # select() in earlier versions of webdriver
        break

def click_input(driver, click_attribute, click_value):

    # Find the radio button input by attribute and value
    checkbox = driver.find_element(By.CSS_SELECTOR, f'input[id="{click_attribute}"]')

    # Move to the label element to ensure it is in view
    ActionChains(driver).move_to_element(checkbox).perform()
    
    # Click the span element
    checkbox.click()

def input_data(driver, data):
    data_inputted = False  # Flag to check if any data is inputted
    for row in data:
        attribute_id = row['ATTRIBUTE']
        attribute_value = row['VALUE']
        value_type = row['VALUE_TYPE']
        element = driver.find_element(By.ID, attribute_id)
        if value_type == 'CLASSIC':
            try:
                classic_input(driver,attribute_id,attribute_value)
            except NoSuchElementException:
                print('Error inputing' + str(attribute_value))
                print(attribute_id)
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
        elif value_type == 'CLICK':
            try:
                click_input(driver, attribute_id, attribute_value)
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
    create_draft(driver)
    time.sleep(5)
    which_page_are_we_in = 0
    data = []
    with open(r"C:\Users\Kenzo Noguera\Desktop\APP PROJECT\Code\Selenium_Version\Curridabat Torres de Granadilla\Curridabat Torres de Granadilla_OMNI_Data.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
        #print('Data---------->')
        #print(data)
    driver.implicitly_wait(5)    
    print('Data Received')
    while which_page_are_we_in < 4:
        get_elements_and_input_them(driver,which_page_are_we_in,data)
        print('Data Processed')
        which_page_are_we_in = which_page_are_we_in + 1
    input("Press Enter to exit...")
if __name__ == '__main__':
    main()



