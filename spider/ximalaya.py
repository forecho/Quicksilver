# !/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
from podgen import Media, Podcast, Person, Category, htmlencode
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz


class Ximalaya():
    def __init__(self, album_id):
        self.podcast = None
        self.album_id = album_id
        self.url = 'http://www.ximalaya.com/album/%s/' % album_id
        self.header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self.url,
            'Cookie': '_ga=GA1.2.1628478964.1476015684; _gat=1',
        }

    def album(self):

        page = requests.get(self.url, headers=self.header)
        soup = BeautifulSoup(page.content, "lxml")

        # 初始化
        self.podcast = Podcast()
        self.podcast.name = soup.find('div', 'detailContent_title').get_text()
        self.podcast.authors.append(Person("Powered by forecho", 'caizhenghai@gmail.com'))
        self.podcast.website = self.url
        self.podcast.copyright = 'cc-by'
        self.podcast.description = soup.find('div', 'mid_intro').get_text()
        self.podcast.language = 'cn'
        self.podcast.image = soup.find('a', 'albumface180').find('img').get('src').split('!')[0]
        self.podcast.feed_url = 'http://podcast.forecho.com/ximalaya/%s.rss' % self.album_id
        self.podcast.category = Category('Technology', 'Podcasting')
        self.podcast.explicit = False
        self.podcast.complete = False
        self.podcast.owner = Person("forecho", 'caizhenghai@gmail.com')

        sound_ids = soup.find('div', class_='personal_body').get('sound_ids').split(',')
        for sound_id in sound_ids:
            self.detail(sound_id)
        # 生成文件
        # print self.podcast.rss_str()
        self.podcast.rss_file('ximalaya/%s.rss' % self.album_id, minimize=True)

    def detail(self, sound_id):
        detail_url = 'http://www.ximalaya.com/tracks/%s.json' % sound_id
        response = requests.get(detail_url, headers=self.header)
        item = json.loads(response.content)

        episode = self.podcast.add_episode()
        episode.id = str(item['id'])
        episode.title = item['title']
        episode.image = item['cover_url_142'].split('?')[0]
        episode.summary = item['intro']
        episode.link = 'http://www.ximalaya.com/sound/%d' % item['id']
        episode.authors = [Person("forecho", 'caizhenghai@gmail.com')]
        episode.publication_date = self.reduction_time(item['time_until_now'], item['formatted_created_at'])
        episode.media = Media(item['play_path_64'], 454599964)
        print item['title']

    # 时间转换 第一个参数是  "3年前", "12月11日 17:00"
    @staticmethod
    def reduction_time(time_until_now, created_at):
        reduction_year = datetime.now().year
        if '年前' in time_until_now:
            year = int(time_until_now.split('年前')[0])
            reduction_year = (datetime.today() - relativedelta(years=year)).year
        elif '月前' in time_until_now:
            month = int(time_until_now.split('月前')[0])
            reduction_year = (datetime.today() - relativedelta(months=month)).year
        elif '天前' in time_until_now:
            day = int(time_until_now.split('天前')[0])
            reduction_year = (datetime.today() - relativedelta(days=day)).year

        date = datetime.strptime(created_at, "%m月%d日 %H:%M")
        return datetime(reduction_year, date.month, date.day, date.hour, date.second, tzinfo=pytz.utc)
