from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import csv

APOLLO_IO_API_URL = ''
ADS_TRANSPARENCY_CENTER_DEFAULT_URL = 'https://adstransparency.google.com/advertiser/AR15992851274060005377?region=US'

UNIVERSAL_WAIT = 5

def initialize_webdriver():
    driver = webdriver.Chrome(service=Service(executable_path='./chromedriver.exe'))

    return driver

def get_domains_from_apollo():
    '''
    Handles the collection of domain information from the prebuilt Apollo.io list
    '''
    return

def check_ads_transparency(businesses):
    '''
    Launches a Selenium webdriver session in order to collect information about ad copy for the collected domains
    '''

    driver = initialize_webdriver()
    
    driver.get(ADS_TRANSPARENCY_CENTER_DEFAULT_URL)

    for business in businesses:
        WebDriverWait(driver, UNIVERSAL_WAIT).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/root/advertiser-page/div[2]/search/div[2]/div/search-input/div/material-input/div[1]/div[1]/label/input')))
        input_box = driver.find_element(By.XPATH, '/html/body/div[3]/root/advertiser-page/div[2]/search/div[2]/div/search-input/div/material-input/div[1]/div[1]/label/input')
        input_box.send_keys(business['name'])
        
        WebDriverWait(driver, UNIVERSAL_WAIT).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/root/advertiser-page/div[2]/search/div[2]/div/search-input/div/div/div[1]/material-select/div/div/div/material-select-item[1]/dynamic-component/search-suggestion-renderer')))
        suggested_advertiser = driver.find_element(By.XPATH, '/html/body/div[3]/root/advertiser-page/div[2]/search/div[2]/div/search-input/div/div/div[1]/material-select/div/div/div/material-select-item[1]/dynamic-component/search-suggestion-renderer')
        ActionChains(driver).move_to_element(suggested_advertiser).click().perform()

        time.sleep(5)
        ad_creatives = driver.find_elements(By.XPATH, '/html/body/div[3]/root/advertiser-page/div[2]/creative-grid/priority-creative-grid/creative-preview')
        for creative in ad_creatives:
            try:
                image = creative.find_element(By.TAG_NAME, 'img')
                image_url = image.get_attribute('src')
                business['ad_copy_list'].append(image_url)
                print(image_url)
            except NoSuchElementException:
                print('Ad is in iframe, skipping to next..')
                continue

    return businesses

def dump_into_csv(businesses):
    '''
    Handles the dumping of the scraped ad copy into a CSV file that will then be sent to the client
    '''
    max_ad_copy = 0
    for business in businesses:
        if len(business['ad_copy_list']) > max_ad_copy:
            max_ad_copy = len(business['ad_copy_list'])

    current_datetime = datetime.now()
    with open(f'./output/{current_datetime.year}-{current_datetime.month}-{current_datetime.day}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['advertiser_disclosed_name', 'advertiser_id']
        for num in range(max_ad_copy):
            fieldnames.append(f'ad_copy_{num + 1}')
        
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for business in businesses:
            row_obj = {
                'advertiser_disclosed_name': business['name'],
                'advertiser_id': business['advertiser_id'],
            }
            for idx, each in enumerate(business['ad_copy_list']):
                row_obj[f'ad_copy_{idx + 1}'] = each

            writer.writerow(row_obj)
    return

if __name__ == '__main__':
    businesses = get_domains_from_apollo()
    businesses = check_ads_transparency(businesses)
    dump_into_csv(businesses)