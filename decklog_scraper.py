# Decklog scrapper Elijah Maron February 20th 2025
# Selenium powered webscraper for automatically downloading images of cards from a supplied deck log

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import os

#initialise a headless browser driver
opts = Options()
opts.add_argument('--headless')
browser = Firefox(options=opts)


base_url = "https://decklog-en.bushiroad.com/view/"

print("Enter a Decklog code (EN Decklog only):")
code = input().upper()

#navigate to the decklog website
browser.get(base_url + code)
print('fetching page')

#wait for the dynamic elements to load
try:
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-view-item.is-select')))
except TimeoutError:
    print("page not loading in time")

print("cards loading")
cards = browser.find_elements(By.CLASS_NAME, 'card-view-item.is-select')
i = str(len(cards) + 23)
final_card_id = 'card-view-'+str(len(cards) + 23)
final_card_view = browser.find_element(By.ID, final_card_id)
final_card = cards[len(cards)-1]

#wait for the final card to be made visible
try:
    element = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.ID, final_card_id)))
except TimeoutError:
    print("page not loading in time")


#ensure all images are loaded before starting to download
try:
   for i in range(len(cards)):
        card_id = 'card-view-'+str(i+24)
        card_view = browser.find_element(By.ID, card_id)
        browser.execute_script("arguments[0].scrollIntoView(true);", card_view)
        element = WebDriverWait(browser, 25).until(EC.text_to_be_present_in_element_attribute((By.ID, card_id), 'src', 'en.cf'))
except TimeoutError:
    print("page not loading in time")

#create a folder for the images
path = './('+code+')' + re.search(r"(^Deck Name.+deck$)",browser.find_element(By.CLASS_NAME, 'views-view.container').text, re.MULTILINE).group()[11:-6]
os.mkdir(path)

#download each image
for card in cards:
    img_data = requests.get(card.get_attribute('src')).content
    with open(path +'/'+ card.get_attribute('alt') + '.png', 'wb') as handler:
        handler.write(img_data)

browser.close()
quit()