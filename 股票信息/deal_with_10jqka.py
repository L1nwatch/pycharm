#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 处理同花顺

http://stockpage.10jqka.com.cn/000629/
http://stockpage.10jqka.com.cn/realHead_v2.html#hs_000629
http://d.10jqka.com.cn/v2/realhead/hs_000629/last.js
"""
import re
import time
from selenium import webdriver

__author__ = '__L1n__w@tch'

browser = None


def get_prices_using_number(number):
    """
    根据股票代码,打印出日 K 线里面最低、最高、当前价格
    :param number:
    :return:
    """
    global browser
    browser.get("http://stockpage.10jqka.com.cn/realHead_v2.html#{}".format(number))
    cur_result = re.findall(r'<span class="price" id="hexm_curPrice">(.*)</span>', browser.page_source)[0]

    try_times = 0
    while cur_result == "--":
        time.sleep(1)
        cur_result = re.findall(r'<span class="price" id="hexm_curPrice">(.*)</span>', browser.page_source)[0]
        if 'id="quote_header2" style="display:none"' not in browser.page_source:
            print("[-] 股票代码: {}, 已经停牌".format(number))
            browser.refresh()
            try_times += 1
        if try_times > 3:
            return None

    browser.get("http://stockpage.10jqka.com.cn/HQ_v4.html#{}".format(number))
    time.sleep(1)
    for each_element in browser.find_elements_by_class_name("kline-type"):
        if each_element.text == "日K线":
            each_element.click()
            break

    while "hxc3-klineprice-min" not in browser.page_source:
        time.sleep(1)

    max_result = re.findall(r'<div class="hxc3-klineprice-max"[^>]*>([^<]*)</div>', browser.page_source)[0]
    min_result = re.findall(r'<div class="hxc3-klineprice-min"[^>]*>([^<]*)</div>', browser.page_source)[0]

    print("[*] 股票代码: {},  当前价为: {}, 最高价为: {}, 最低价为: {}".format(number, cur_result, max_result, min_result))

    with open("test.html", "w") as f:
        f.write(browser.page_source)


def get_all_number():
    """
    访问 数据中心 最近的 业绩预告, 获取所有股票代码
    :return:
    """
    global browser

    url = "http://data.10jqka.com.cn/financial/yjyg/"
    browser.get(url)
    result = re.findall('<a href="http://stockpage.10jqka.com.cn/\d*/finance/" target="_blank">(\d*)</a>',
                        browser.page_source)
    return result


def main():
    global browser
    browser = webdriver.Chrome(
        "/Users/L1n/Desktop/Code/Python/my_blog_source/virtual/selenium/webdriver/chromedriver",
    )

    finish_list = list()
    with open("result.txt") as f:
        for each_line in f:
            finish_list.append(each_line[13:19])

    numbers = get_all_number()
    for each_number in numbers:
        if each_number in finish_list:
            continue
        get_prices_using_number("hs_{}".format(each_number))

    browser.quit()


if __name__ == "__main__":
    main()
