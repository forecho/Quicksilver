# !/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
from podgen import Media, Podcast, Person, Category
from datetime import datetime
import pytz


class Ximalaya():
    def __init__(self, album_id):
        self.podcast = None
        self.album_id = album_id
        self.album_list_api = "http://www.ximalaya.com/revision/play/album?albumId={}&pageNum=1&sort=1&pageSize=999".format(album_id)
        self.album_url = 'http://www.ximalaya.com/album/%s' % album_id
        self.header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self.url,
            'Cookie': '_ga=GA1.2.1628478964.1476015684; _gat=1',
        }

    def album(self):
        page = requests.get(self.album_url, headers=self.header)
        soup = BeautifulSoup(page.content, "lxml")

        # 初始化
        self.podcast = Podcast()
        self.podcast.name = soup.find('h1', 'title').get_text()
        self.podcast.authors.append(Person("Powered by forecho", 'caizhenghai@gmail.com'))
        self.podcast.website = self.url
        self.podcast.copyright = 'cc-by'
        self.podcast.description = soup.find('div', 'album-intro').get_text()
        self.podcast.language = 'cn'
        self.podcast.image = soup.find('div', 'album-info').find('img').get('src').split('!')[0]
        self.podcast.feed_url = 'http://podcast.forecho.com/ximalaya/%s.rss' % self.album_id
        self.podcast.category = Category('Technology', 'Podcasting')
        self.podcast.explicit = False
        self.podcast.complete = False
        self.podcast.owner = Person("forecho", 'caizhenghai@gmail.com')

        album_list_content = requests.get(self.album_list_api).content
        album_list_data = json.loads(album_list_content)
        count = len(album_list_data['data']['tracksAudioPlay'])
        for each in album_list_data['data']['tracksAudioPlay']:
            page_info = requests.get('http://www.ximalaya.com/%s' % each['trackUrl'], headers=self.header)
            soup_info = BeautifulSoup(page_info.content, "lxml")
            episode = self.podcast.add_episode()
            episode.id = str(index['id'])
            episode.title = each['trackName']
            print self.podcast.name + '=====' + each['trackName']
            image = each['trackCoverPath'].split('?')[0]
            if (image[-4:] == '.gif'):
                episode.image = self.podcast.image
            else:
                episode.image = image
            episode.summary = soup_info.find('div', 'intro').get_text()
            episode.link = 'http://www.ximalaya.com/%s' % each['albumUrl']
            episode.authors = [Person("forecho", 'caizhenghai@gmail.com')]
            episode.publication_date = self.reduction_time(soup_info.find('span', 'time').get_text())
            episode.media = Media(each['src']), each['duration'])
            episode.position = count - index['id'] + 1
        # 生成文件
        # print self.podcast.rss_str()
        self.podcast.rss_file('ximalaya/%s.rss' % self.album_id, minimize=True)

    # 时间转换
    @staticmethod
    def reduction_time(created_date):
        timestamp = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
        return datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute,
                        tzinfo=pytz.utc)