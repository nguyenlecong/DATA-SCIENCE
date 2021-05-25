"""
-Truy cập từng bài viết bằng link từ file txt:
    -Đăng nhập nếu là bài viết cá nhân hoặc trong group
    -Không cần đăng nhập với bài viết trên fanpage
        -bấm 'lúc khác'
        -bấm 'xyz bình luận'
    -Với mỗi bài viết:
        -hiển thị tất cả bình luận bằng cách bấm 'xem thêm bình luận' nếu có.
        -bấm 'phản hồi' nếu có.
        -bấm 'xem thêm các phản hồi', nếu có nhiều phản hồi.
        -với mỗi bình luận:
            -bấm "xem thêm" để xem hết bình luận nếu bình luận dài.
        -lấy tất cả text của bình luận.
        -ghi vào file csv.
"""

# -*- coding: utf-8 -*-
import re
import csv
import random
import pandas as pd
from time import sleep
from selenium import webdriver
from underthesea import word_tokenize
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Giả lập gia diện và tắt thông báo của Chrome
def open_browser():
    browser = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    browser.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(chrome_options=browser)
    sleep(random.randint(5,10))

    return browser

# Đăng nhập vào facebook
def login(browser):
    browser.get('https://www.facebook.com/')
    sleep(random.randint(5,10))

    fill_username = browser.find_element_by_id('email')
    fill_username.send_keys('caoquocdat06@gmail.com')
    sleep(random.randint(5,10))

    fill_password = browser.find_element_by_id('pass')
    fill_password.send_keys('diepvien009')
    sleep(random.randint(5,10))

    fill_password.send_keys(Keys.ENTER)
    sleep(random.randint(5,10))

# Load link
def load(browser, link):
    browser = browser.get(link)
    sleep(random.randint(5,10))

    return browser

# "Lúc khác"
def another_time(browser):
    try:
        another_time = browser.find_element_by_class_name('_3j0u')
        another_time.click()
        sleep(random.randint(5,10))
    except:
        pass

# "Bình luận"
def show_comment(browser):
    try:
        try:
            show_cmt = browser.find_element_by_xpath('//*[@id="u_0_u"]/div/div[2]/div[1]/div/div[3]/span[1]/a')
            show_cmt.click()
            sleep(random.randint(5,10))
        except:
            show_cmt = browser.find_element_by_xpath('//*[@id="u_0_1b"]/div/div[2]/div[1]/div/div[3]/span[1]/a')
            show_cmt.click()
            sleep(random.randint(5,10))
    except:
        pass

# Show all comment
def show_all_comments(browser):
    has_more_comments = True
    while has_more_comments:
        try:
            try:
                show_all_cmt = browser.find_element_by_xpath('//div[@class="j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7"]\
                    /div[@class="j83agx80 buofh1pr jklb3kyz l9j0dhe7"]')
                show_all_cmt.click()
                sleep(random.randint(5,10))
            except:
                show_all_cmt = browser.find_element_by_xpath('//span[@class=" _4ssp"]')
                show_all_cmt.click()
                sleep(random.randint(5,10))
        except:
            has_more_comments = False

# Phản hồi
def reply(browser):
    has_Reply = True
    while has_Reply:
        try:
            try:
                reps = browser.find_elements_by_xpath('//div[@class="kvgmc6g5 jb3vyjys rz4wbd8a qt6c0cv9 d0szoon8"]\
                /div[@class="j83agx80 buofh1pr jklb3kyz l9j0dhe7"]')
                for rep in reps:
                    rep.click()
                    sleep(random.randint(5,10))
            except:
                rep = browser.find_element_by_xpath('//div[@class="_4swz _7a9e _7a93"]')
                rep.click()
                sleep(random.randint(5,10))
        except:
            has_Reply = False

# Thêm phản hồi
def more_replies(browser):
    has_more_Replies = True
    while has_more_Replies:
        try:
            more_rep = browser.find_element_by_xpath('//div[@class="l9j0dhe7"]/div[@class="j83agx80 buofh1pr jklb3kyz l9j0dhe7"]')
            more_rep.click()
            sleep(random.randint(5,10))

        except:
            has_more_Replies = False

# See more
def see_more(browser):
    long_comment = True
    while long_comment:
        try:
            try:
                see_more = browser.find_element_by_xpath('//div[@class="ecm0bbzt e5nlhep0 a8c37x1j"]/span/\
                    div[@class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]/div/div')
                see_more.click()
                sleep(random.randint(5,10))
            except:
                see_more = browser.find_element_by_xpath('//a[@class="_5v47 fss"]')
                see_more.click()
                sleep(random.randint(5,10))
        except:
            long_comment = False

# Ghi vào file
def write(browser):
    try:
        comment_content = browser.find_elements_by_xpath("//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']")
    except:
        comment_content = browser.find_elements_by_class_name('_3l3x')

    for comment in comment_content:
        print(comment.text)
    # with open('data/dataset.csv', mode='a', encoding='utf-8', newline='') as file:
    #     for comment in comment_content:
    #         print(comment.text)
    #         writer = csv.writer(file, delimiter=',')
    #         writer.writerow([comment.text, '0'])
    # file.close()

def header():
    df = pd.read_csv('data/data_demo.csv', header=None)
    df.columns = ['Text', 'Sentiment']
    df.to_csv('data/data_demo.csv', index = False)

# Kiểm tra đăng nhập
def check_login(browser, link):  
    try:
        browser.find_element_by_xpath('//span[@class="_39_n _5pb8 o_c3pynyi2g _8o _8s lfloat _ohe"]')
        login = True
    except:
        login = False
    
    return login

if __name__ == "__main__":
    # Test
    browser = open_browser()
    login(browser)

    with open('post_topic_link.txt', "r", encoding="utf-8") as f:
        for line in open('post_topic_link.txt'):
            link = line.rstrip('\n')
            # browser = open_browser()
            broswer = load(browser,link)
            # if check_login(browser, link):
            #     login(browser)
            #     broswer = load(browser,link)
            # another_time(browser)
            # show_comment(browser)
            # show_all_comments(browser)
            # reply(browser)
            # more_replies(browser)
            # see_more(browser)
            write(browser)
            # browser.close()
    browser.close()
    f.close()
    # header()