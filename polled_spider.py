#!/usr/bin/env python
# encoding:utf-8
"""
@author : llh
@software : PyCharm
@times : 2018/12/14 10:32
"""
import pandas as pd
from retry import retry
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import getopt, sys
import time


def get_item_info(soup):
    pre_dict = defaultdict(list)
    title_primary = soup.select("div.rslt > p > a")
    publish_if_primary = soup.select("div.rslt > div.supp > p.details > span")
    year_primary = soup.select("div.rslt > div.supp > p.details")
    author_primary = soup.select("div.rslt > div.supp > p.desc")
    for i in range(165):
        # title
        pre_dict["Title"].append(title_primary[i].get_text())
        pre_dict["Title_URL"].append(title_primary[i].attrs["href"])
        pre_dict["Publish"].append(list(publish_if_primary[i].stripped_strings)[0])
        pre_dict["IF"].append(list(publish_if_primary[i].stripped_strings)[1])
        pre_dict["Year"].append(list(year_primary[i].stripped_strings)[2].split()[1])
        pre_dict["Author"].append(list(author_primary[i].stripped_strings)[0])
    return pre_dict


@retry(tries=5, delay=8)
def get_abstract(urls):
    abstract = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36"}
    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        if len(soup.select("div.abstr > div > p")) == 0:
            abstract.append("None")
        elif len(soup.select("div.abstr > div > p")) >= 1:
            ele = soup.select("div.abstr > div > p")[0].get_text()
            abstract.append(ele)
        time.sleep(5)
    return abstract


def save_dataframe(dict, abstract):
    columns = ["Title", "Author", "Abstract", "Title_URL", "Year", "Publish", "IF"]
    dict["Abstract"] = abstract
    data = pd.DataFrame(dict, columns=columns)
    data.to_csv("polled_cattle_papers.csv", index=False, columns=columns)
    return data.head()


if __name__ == "__main__":
    input_file = None
    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:')
    for op, value in opts:
        if op == "-i":
            input_file = str(value)
            if input_file == "":
                print("ERROR: no input files!")
                sys.exit()
        elif op == "-h":
            print('Usage:')
            print('python polled_spider.py -i PolledCattle.html -o polled_cattle.csv')
            sys.exit()
    html = input_file
    with open(html, "r", encoding="UTF-8") as f:
        response = f.read()
    soup = BeautifulSoup(response, "lxml")
    pre_dict = get_item_info(soup)
    urls = pre_dict["Title_URL"]
    abstract = get_abstract(urls)
    data = save_dataframe(pre_dict, abstract)
    print(data)




