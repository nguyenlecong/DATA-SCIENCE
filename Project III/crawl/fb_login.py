import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 1. khai báo biến broswer - đại diện cho trình duyệt
# browser = webdriver.Chrome(executable_path = 'chromedriver.exe') # Dùng trình duyệt giả lập Chrome

#1a. Tắt thông báo của browser
browser = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
browser.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(chrome_options=browser)
sleep(random.randint(1,5))

# 2. Thử mở một trang web
browser.get('https://www.facebook.com/')
sleep(random.randint(1,5))

# 3. Điển thông tin vào ô username và password
fill_username = browser.find_element_by_id('email')
fill_username.send_keys('caoquocdat06@gmail.com')
sleep(random.randint(1,5))

fill_password = browser.find_element_by_id('pass')
fill_password.send_keys('diepvien009')
sleep(random.randint(1,5))

# 4. Login
fill_password.send_keys(Keys.ENTER)

# 5. Dừng chương trình :
sleep(random.randint(5,10))

# 6. Đóng trình duyệt
browser.close()