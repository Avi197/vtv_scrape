#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup


def url_to_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup


def get_relate(url):
    soup = url_to_soup(url)
    relate_section = soup.find_all('div', {'class': "article-relate"})
    related_news_list = []

    if relate_section is not None:
        for rs in relate_section:
            related = rs.find_all('a')
            for r in related:
                related_news = dict()
                related_news['title'] = r.text.strip()
                related_news['url'] = "https://vietnamnet.vn" + r.get('href')
                related_news_list.append(related_news)
    return related_news_list


def scrape(pages):
    data = []
    news_category = 'thoi-su/'
    page = 1

    # for the 5 news that just there
    url = 'https://vietnamnet.vn/vn/' + news_category
    soup = url_to_soup(url)

    top_1 = soup.find('div', {'class': 'top-one-cate'}).find('h3', {'class': 'm-t-5'}).find('a')
    top_1_news = dict()
    top_1_news['url'] = "https://vietnamnet.vn" + top_1.get('href')
    top_1_news['title'] = top_1.text.strip()
    top_1_news['related_news'] = get_relate(top_1_news['url'])
    data.append(top_1_news)

    top_content = soup.find('div', {'class': "BoxCate BoxStyle5"}).find("ul", {'class': 'height-list va-top'})
    for li in top_content.find_all('li', {'class': 'clearfix'}):
        news = dict()
        news['url'] = "https://vietnamnet.vn" + li.find('a').get('href')
        news['title'] = li.find('a').get('title')
        news['related_news'] = get_relate(news['url'])
        data.append(news)
    # ----------------------------------------------------------------

    while page <= pages:
        url = 'https://vietnamnet.vn/vn/' + news_category + 'trang' + str(page)
        soup = url_to_soup(url)

        content = soup.find('div', {'class': 'list-content list-content-loadmore lagre m-t-20 clearfix'})
        for div in content.find_all('div', {'class': 'clearfix item'}):
            news = dict()
            news['url'] = "https://vietnamnet.vn" + div.find('a').get('href')
            news['title'] = div.find('a').get('title')
            news['related_news'] = get_relate(news['url'])
            data.append(news)

        with open("vnn_with_url_1538p.json", 'w') as json_data_out:
            json.dump(data, json_data_out, ensure_ascii=False, indent=2)
        page += 1


scrape(1538)
