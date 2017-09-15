#coding=utf-8
# Copyright (c) 2016 Kenneth Blomqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

############################
## How to use
############################
# modify google file: the 1st column is the file path, and the 2nd column is the seaching key-word
# modify count, the param is the minimum searching result count.
# sometimes, the final searching number is small, eg. count=500, but only return 28. This may be related to the webdriver, it's a bug, but I don't know how to fix it. Run it again, it returns correctly.

import os
import re
import time
from selenium import webdriver

def ensure_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def largest_file(dir_path):
    def parse_num(filename):
        match = re.search('\d+', filename)
        if match:
            return int(match.group(0))

    files = os.listdir(dir_path)
    if len(files) != 0:
        return max(filter(lambda x: x, map(parse_num, files)))
    else:
        return 0

def fetch_image_urls_google(query, images_to_download):
    image_urls = set()

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome()
    browser.get(search_url.format(q=query))
    def scroll_to_bottom():
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

    image_count = len(image_urls)
    delta = 0
    while image_count < images_to_download:
        print("Found:", len(image_urls), "images")
        scroll_to_bottom()

        images = browser.find_elements_by_css_selector("img.rg_ic")
        for img in images:
            image_urls.add(img.get_attribute('src'))
        delta = len(image_urls) - image_count
        image_count = len(image_urls)

        if delta == 0:
            print("Can't find more images")
            break

        fetch_more_button = browser.find_element_by_css_selector(".ksb._kvc")
        if fetch_more_button:
            browser.execute_script("document.querySelector('.ksb._kvc').click();")
            scroll_to_bottom()

    browser.quit()
    return image_urls

def fetch_image_urls_soso(query, images_to_download):
    image_urls = set()

    search_url = "http://pic.sogou.com/pics?query={q}&di=2&_asf=pic.sogou.com&w=05009900"
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome()
    browser.get(search_url.format(q=query))
    def scroll_to_bottom():
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    image_count = len(image_urls)
    delta = 0
    while image_count < images_to_download:
        print("Found:", len(image_urls), "images")
        scroll_to_bottom()

        images = browser.find_elements_by_xpath('//div[@id="imgid"]/ul/li/a/img')
        for img in images:
            image_urls.add(img.get_attribute('src'))
        delta = len(image_urls) - image_count
        image_count = len(image_urls)

        if delta == 0:
            print("Can't find more images")
            break

    browser.quit()
    return image_urls

if __name__ == '__main__':
    count = 300
    is_google = False

    savepath = os.path.abspath('./images/')

    query = []
    label = []
    with open('./google') as f:
        lines = f.readlines()
        for line in lines:
            re = line.strip().split('\t')
            query.append(re[1])
            label.append(re[0])
    f.close()

    ensure_directory(savepath)

    for i, val in enumerate(query):
        query_directory = savepath + "/"+ label[i] + "/"
        ensure_directory(query_directory)

        if is_google:
            image_urls = fetch_image_urls_google(val, count)
        else:
            image_urls = fetch_image_urls_soso(val, count)

        print("image count", len(image_urls))
        cnt = 0
        os.chdir(os.path.abspath(query_directory))
        for url in image_urls:
            if url is None:
                continue
            # print url
            if is_google:
                curl = 'curl -o ' + '\'%s_%04d.jpg\'' % (
                    label[i], cnt) + ' --insecure ' + '\''+url+'\'' + ' --socks5-hostname 127.0.0.1:1080\n'
            else:
                curl = 'curl -o ' + '\'%s_%04d.jpg\'' % (
                    label[i], cnt) + ' --insecure ' + '\'' + url + '\'\n'
            os.system(curl)
            cnt += 1