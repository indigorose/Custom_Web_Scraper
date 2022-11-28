# Custom Web Scraper
import selenium as selenium
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chromedriver_path = "/Users/robertsonkla/Documents/Coding_Projects/Python/chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver_path)

forms_url = "https://forms.gle/JRCPLGqnjrzQ8W2d8"

zoopla_url = "https://www.zoopla.co.uk/for-sale/property/se1/?page_size=25&view_type=list&q=SE1%20%20Waterloo%2C" \
             "%20Bermondsey%2C%20South%20Bank%2C%20The%20Borough%2C%20...&radius=0&results_sort=highest_price" \
             "&search_source=refine "

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.102 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
# Check the header information, now that I have upgraded

response = requests.get(url=zoopla_url, headers=headers)
price_results = response.text

soup = BeautifulSoup(price_results, 'lxml')
driver.get(forms_url)

full_price = soup.find_all("div", class_="c-bTssUX")
price_list = [price.get_text() for price in full_price]
# test
# print(full_price_list)
full_price_list = [re.split('£ |,|/|\\+', price)[1:3] for price in price_list]
full_price = [",".join(price) for price in full_price_list]

# Find the property addresses
prop_soup = soup.find_all('address', class_='c-eFZDwI')
prop_addresses = [address.get_text() for address in prop_soup]
# test
# print(prop_addresses)

start_link = 'https://zoopla.co.uk/for-sale'

links_soup = soup.find_all('a', class_='c-hhFiFN')
zoopla_links = [link.get('href') for link in links_soup]
zoopla_links_list = zoopla_links[::2]

prop_links_list = [link.replace("/b", start_link) for link in zoopla_links]

for (address, price, link) in zip(prop_addresses, price_list, zoopla_links_list):
    # add info to the sheet.
    time.sleep(3)
    address_test = driver.find_element(By.XPATH, value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div["
                                                       "2]/div/div[1]/div/div[1]/input")
    # address_test.send_keys("Indigo")
    full_price_test = driver.find_element(By.XPATH, value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div["
                                                            "2]/div/div[1]/div/div[1]/input")
    # rental_price_test.send_keys("1234")
    property_link_test = driver.find_element(By.XPATH, value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div["
                                                             "2]/div/div[1]/div/div[1]/input")
    # property_link_test.send_keys("Indigo@gmail.com")
    submit_button = driver.find_element(By.XPATH, value="//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div["
                                                        "1]/div/span/span")
    # submit_button.click()
    address_test.send_keys(address)
    full_price_test.send_keys(price)
    property_link_test.send_keys(link)
    submit_button.click()
    driver.back()
