import csv
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

browser = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2} # Tắt thông báo Chrome
browser.add_experimental_option("prefs",prefs)

# Ẩn cửa sổ browser
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options, executable_path=r'D:\Tai Lieu\HUST-Study\20202\Tích hợp dữ liệu\project\crawl\chromedriver.exe')

browser.get('https://didongviet.vn/apple')

links = []

item1 = browser.find_elements_by_xpath('//li[@class="item product product-item-new product-item  "]/a')
for item in item1:
    link = item.get_attribute('href')
    links.append(link)

item2 = browser.find_elements_by_xpath('//li[@class="item product product-item-new product-item "]/a')
for item in item2:
    link = item.get_attribute('href')
    links.append(link)

data = {'Tên': [], 'Link': [], 'Giá': [], 'Ảnh': [], 'Màu': [], 'Màn hình': [], 'Camera sau': [], 'Camera trước': [], 'Hệ điều hành - CPU': [], 'Bộ nhớ - Lưu trữ': [], 'Kết nối': [], 'Thông tin pin - Sạc': []}
detail = list(data.keys())
detail = detail[5:13]

def extract(link):
    browser.get(link)

    # Link
    data['Link'].append(link)

    # Name
    name = browser.find_element_by_xpath('//div[@class="page-title-wrapper product"]/h1/span').text
    data['Tên'].append(name)

    # Price
    price = browser.find_element_by_class_name('price').text.replace('.', '').replace('₫', '').replace(' ', '')
    data['Giá'].append(price)

    # Color
    color = []
    colors = browser.find_elements_by_xpath('//div[@class="  control-option"]/*/span[1]')
    for c in colors:
        color.append(c.text)
    color = ', '.join(str(i) for i in color)
    data['Màu'].append(color)

    # Image
    img = browser.find_element_by_xpath('//div[@class="nav-gallery-right"]/img').get_attribute('src')
    data['Ảnh'].append(img)

    # Detail
    att_table = browser.find_element_by_xpath('//p[@class="showmoreattribute"]/a')
    browser.execute_script("arguments[0].click();", att_table)

    att = []
    key = browser.find_elements_by_xpath('//div[@class="modal-attribute"]/div//div[2]/div/div/*/div[1]')
    value = browser.find_elements_by_xpath('//div[@class="modal-attribute"]/div//div[2]/div/div/*/div[2]')
    for i in range(len(key)):
        k = key[i].text
        att.append(k)
        if k in detail:
            v = value[i].text.replace('\n', ', ')
            data[k].append(v)
    for i in range(len(detail)):
        if detail[i] not in att:
            data[detail[i]].append('')

    return data

if __name__ == '__main__':
    for i in range(len(links)):
        print(i)
        data = extract(links[i])

    browser.quit()

    df = pd.DataFrame.from_dict(data)
    df.to_csv('schedule/schedule.csv', index = False)