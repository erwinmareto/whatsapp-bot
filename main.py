from selenium import webdriver
import time

url = "https://web.whatsapp.com/"
chrome_driver_path = 'C:\Development\chromedriver.exe'

driver = webdriver.Chrome(chrome_driver_path)

web_page = driver.get(url)

time.sleep(30)

chat_boxes = driver.find_elements_by_class_name("_3OvU8")

for contact in chat_boxes:
    if "Papa" in contact.text:
        papa = contact
    else:
        print(contact.text)

papa.click()


time.sleep(60)

for i in range(2):
    driver.execute_script("window.scrollTo(0, -1080)")

time.sleep(10)

links = driver.find_elements_by_css_selector("._33LGR a")

for link in links:
    # if links.index(link) % 2 != 0:
    #     print(link.text)

    print(link.text)
