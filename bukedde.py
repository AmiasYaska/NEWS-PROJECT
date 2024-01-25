from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.bukedde.co.ug/'
driver.get(url)

time.sleep(2)

data = []  # Store all scraped data in a list
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        new_height = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".col-xl-3"))
        ).location["y"]

    except:
        break

    if new_height == last_height:
        break
    else:
        last_height = new_height

    # Extract text from all selectors and append to data list
    for titles in [(".home_article_tiltle", "Title"), (".text-wrap", "Title"),
                   (".heading", "Title on photo")]:
        selector, key = titles  # Unpack the tuple

        for title_element in driver.find_elements(By.CSS_SELECTOR, selector):  # Pass selector separately
            data.append({key: title_element.text})

with open('bukedde_news.json', 'w') as f:
    json.dump(data, f, indent=4)  # Indent for readability

print("Data saved to bukedde_news.json")

driver.quit()
