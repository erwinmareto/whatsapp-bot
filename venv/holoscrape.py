from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time

url = "https://www.youtube.com/channel/UC6eWCld0KwmyHFbAqK3V-Rw/channels"
chrome_driver_path = "C:/Development/chromedriver.exe"

driver = webdriver.Chrome(chrome_driver_path)

web_page = driver.get(url)

time.sleep(5)

pixels = 1080
for z in range(3):
    driver.execute_script(f"window.scrollTo({z}, {1080 + pixels * z})")
    time.sleep(2)
    driver.execute_script(f"window.scrollTo(1080, 3000)")

driver.execute_script("window.scrollTo(0, 0)")

channels = driver.find_elements_by_id("channel-info")
channel_names = driver.find_elements_by_css_selector("#channel-info #title")
sub_counts = driver.find_elements_by_id("thumbnail-attribution")
print(len(channels))
print(len(channel_names))
print(len(sub_counts))
for name in channel_names:
    print(f"{name.text}({channel_names.index(name)})")

pixels = 500
rounds = 0
for n in range(0, len(channel_names)):
    #Channel List
    time.sleep(5)

    try:
        print(channel_names[n].text)
        print(sub_counts[n].text)
        time.sleep(5)
        channel_names[n].click()
    except StaleElementReferenceException:
        for num in range(3):
             driver.execute_script(f"window.scrollTo({num}, {1080 + pixels * num})")
             time.sleep(2)
             driver.execute_script(f"window.scrollTo(1080, 3000)")
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(10)
        channels = driver.find_elements_by_id("channel-info")
        channel_names = driver.find_elements_by_css_selector("#channel-info #title")
        sub_counts = driver.find_elements_by_id("thumbnail-attribution")
        print(channel_names[n].text)
        print(sub_counts[n].text)
        time.sleep(5)
        channel_names[n].click()

    time.sleep(5)

    #about page
    about = driver.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[6]/div')
    about.click()

    time.sleep(5)
    try:
        driver.execute_script("window.scrollTo(0, 1080)")
        link_box = driver.find_element_by_css_selector("#link-list-container a")
    except NoSuchElementException:
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, 1080)")
        link_box = driver.find_element_by_css_selector("#link-list-container a")

    link_box.click()

    time.sleep(3)

    #Twitter
    driver.switch_to.window(driver.window_handles[1])

    try:
        followers = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span')
    except NoSuchElementException:
        try:
            time.sleep(5)
            followers = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span')
        except NoSuchElementException:
            try:
                #Anya and Ollie Exception
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                link_box = driver.find_elements_by_css_selector("#link-list-container a")
                link_box[1].click()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(10)
                followers = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span')
            except NoSuchElementException:
                #Iofi Exception
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                link_box = driver.find_elements_by_css_selector("#link-list-container a")
                link_box[5].click()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(10)
                followers = driver.find_element_by_xpath(
                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span')

    print(followers.text)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    #Undo to channel list
    for r in range(2):
        driver.back()


    print(f"Index: {n}")


