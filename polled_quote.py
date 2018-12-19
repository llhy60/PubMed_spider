#!/usr/bin/env python
# encoding:utf-8
"""
@author : llh
@software : PyCharm
@times : 2018/12/19 10:44
"""
import pandas as pd
from selenium import webdriver
import time, re


def find_quote(keys):
    browser = webdriver.Chrome('D:\\Program Files\\selenium_driver\\chromedriver.exe')
    browser.get("https://scholar.google.com.hk/schhp?hl=zh-CN")
    time.sleep(3)
    browser.find_element_by_css_selector("#gs_hdr_tsi").send_keys(keys)
    browser.find_element_by_css_selector("#gs_hdr_tsb").click()
    text = browser.find_element_by_css_selector("#gs_res_ccl_mid > div > div > div.gs_fl > a:nth-child(3)").text
    if text:
        reg_str = '.*?：(\d+)'
        mat = re.match(reg_str, text)
        if mat:
            quote = int(mat.group(1))
        else:
            quote = 0
    else:
        quote = 0
    time.sleep(2)
    browser.close()
    return quote


if __name__ == "__main__":
    data = pd.read_csv("polled_cattle.csv")
    titles = data["Title"]
    quotes = []
    for title in titles:
        quote = find_quote(title)
        quotes.append(quote)
        time.sleep(3)
    data["quote"] = quotes
    data.to_csv("polled_cattle_papers.csv")
    print("That's OK!")
