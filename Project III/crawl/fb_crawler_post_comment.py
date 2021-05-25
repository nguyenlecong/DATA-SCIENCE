# -*- coding: utf-8 -*-
# 1. Import thư viện
import re
import csv
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from underthesea import word_tokenize

# 2. Khai báo biến broswer - đại diện cho trình duyệt
browser = webdriver.Chrome(executable_path = 'chromedriver.exe') # Dùng trình duyệt giả lập Chrome

# 3. Mở URL của Post
browser.get('https://www.facebook.com/photo?fbid=2490810964474834&set=a.1665540343668571')
sleep(random.randint(5,10))

# 4. Tắt "xem thêm"
another_time = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[4]/a')
another_time.click()
sleep(random.randint(5,10))

# 5. Ghi nội dung post ra màn hình
post_content = browser.find_element_by_id('js_2')
print('* Nội dung bài viết:', post_content.text)
sleep(random.randint(5,10))

# 6. Hiển thị comment
comment_link = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div/div[2]/div[1]/div/div[3]/span/a')
comment_link.click()
sleep(random.randint(5,10))

# 6a. Hiển thị thêm comment
more_comment_link = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div/div[3]/div[1]/div/a/div')
more_comment_link.click()
sleep(random.randint(5,10))

# 7. Tìm tất cả các comment
# -> lấy tất cả thẻ div có thuộc tính aria-label="Bình luận"
comment_list = browser.find_elements_by_xpath('//div[@aria-label="Bình luận"]')
sleep(random.randint(5,10))

# 8. Ghi nội dung comment ra màn hình
writer = csv.writer(open('test.csv', 'w', newline='', encoding="utf-8"))
writer.writerow(['Comment', 'Sentiment'])
for comment in comment_list:
    comment_poster = comment.find_element_by_class_name('_6qw4')
    comment_content = comment.find_element_by_class_name('_3l3x')
    
    # 8a. Ghi comment vào file csv
    writer.writerow([comment_content.text, ''])

# 9. Dừng chương trình 5<x<10 giây:
sleep(random.randint(5,10))

# 10. Đóng trình duyệt
browser.close()