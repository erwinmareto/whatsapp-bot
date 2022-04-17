from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas

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


def add_to_dataframe(data_num, data_list):
    if "M" in data_num.text.split()[0]:
        split_number = data_num.text.split("M")
        data_list.append(float(split_number[0]) * 1000)
    elif "K" in data_num.text.split() or "K" in data_num.text.split()[0]:
        split_number = data_num.text.split("K")
        try:
            data_list.append(float(split_number[0]))
        except ValueError:
            new_num = split_number[0].split("K")
            data_list.append(float(new_num))
    else:
        split_number = data_num.text.split("万")
        data_list.append(float(split_number[0]) * 10)


pixels = 500
rounds = 0
youtube_channel_names = []
youtube_sub_count = []
twitter_follower_count = []

for n in range(0, len(channel_names), 33):
    #Channel List
    time.sleep(5)

    try:
        print(channel_names[n].text)
        print(sub_counts[n].text.split()[0])
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

    #Adding channel names and sub count data into empty list for dataframe
    new_channel = channel_names[n].text.split()
    try:
        youtube_channel_names.append(f"{new_channel[0]} {new_channel[1]}")
    except IndexError:
        new_channel = channel_names[n].text.split("。")
        youtube_channel_names.append(f"{new_channel[0]} {new_channel[1]}")

    #Getting Rid of "M" and "K" from number
    add_to_dataframe(sub_counts[n], youtube_sub_count)

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
                # Exception for Anya and Ollie
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                link_box = driver.find_elements_by_css_selector("#link-list-container a")
                link_box[1].click()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(10)
                followers = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span')
            except NoSuchElementException:
                # Exception for Iofi
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

    #Adding Twitter follower data into list
    add_to_dataframe(followers, twitter_follower_count)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    #Go to channel list
    if n == 33:
        channels_page = driver.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[5]/div')
        channels_page.click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 1080)")
        time.sleep(3)
        channels = driver.find_elements_by_id("channel-info")
        channel_names = driver.find_elements_by_css_selector("#channel-info #title")
        sub_counts = driver.find_elements_by_id("thumbnail-attribution")

        for k in range(0, len(channel_names)):
            if "Koyori" in channel_names[k].text.split():
                print(channel_names[k].text)
                print(sub_counts[k].text)
                new_channel = channel_names[k].text.split()
                youtube_channel_names.append(f"{new_channel[0]} {new_channel[1]}")

                add_to_dataframe(sub_counts[k], youtube_sub_count)

                channel_names[k].click()
                time.sleep(5)
                about = driver.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[6]/div')
                about.click()

                time.sleep(5)

                driver.execute_script("window.scrollTo(0, 1080)")
                link_box = driver.find_element_by_css_selector("#link-list-container a")

                link_box.click()

                time.sleep(5)

                driver.switch_to.window(driver.window_handles[1])
                followers = driver.find_element_by_xpath(
                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span')
                print(followers.text)
                split_follower = followers.text.split("K")
                twitter_follower_count.append(float(split_follower[0]))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                for r in range(5):
                    driver.back()
    else:
        for r in range(2):
            driver.back()

    print(f"Index: {n}")

#Create dataframe and turn into csv
data_dict = {
    "Channels": youtube_channel_names,
    "YT Sub Count": youtube_sub_count,
    "Twitter Follower": twitter_follower_count
}

data = pandas.DataFrame(data_dict)

data["Difference"] = (data["YT Sub Count"] - data["Twitter Follower"])

data.to_csv("Hololive sub count vs followers.csv")

frame = pandas.read_csv("Hololive sub count vs followers.csv")

print(frame.head())

