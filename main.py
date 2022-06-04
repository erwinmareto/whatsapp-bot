from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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


time.sleep(30)

for i in range(2):
    driver.execute_script("window.scrollTo(0, -1080)")

time.sleep(10)

links = driver.find_elements_by_css_selector("._33LGR a")

download_links = []

for link in links:
    if links.index(link) % 2 == 0:
        download_links.append(link.text)
        # print(link.text)

    print(link.text)
print(download_links)


for down_link in download_links:
    driver.get("https://getx.topsandtees.space/PXAeoljYgO")

    time.sleep(5)

    if "youtu.be" in down_link:

        text_field = driver.find_element_by_xpath("/html/body/main/div/section/form/div/input[1]")
        text_field.send_keys(down_link)
        text_field.send_keys(Keys.ENTER)

        driver.switch_to.window(driver.window_handles[0])
        download_button = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div[1]/div/a")
        download_button.click()

        time.sleep(20)

        try:
            down_button = driver.find_element_by_xpath("/html/body/main/div/div/p/span")
            down_button.click()
        except NoSuchElementException:
            time.sleep(20)
            down_button = driver.find_element_by_xpath("/html/body/main/div/div/p/span")
            down_button.click()

        print(down_link)


