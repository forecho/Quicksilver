# !/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
from podgen import Media, Podcast, Person, Category
from datetime import datetime
import traceback
import pytz
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal
from helper.humanize_time import humanize_time

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
            'Referer': self.album_url,
            'Cookie': '_ga=GA1.2.1628478964.1476015684; _gat=1',
        }

    def album(self):
        page = requests.get(self.album_url, headers=self.header)
        soup = BeautifulSoup(page.content, "lxml")

        # 初始化
        self.podcast = Podcast()
        self.podcast.name = soup.find('h1', 'title').get_text()
        self.podcast.authors.append(Person("Powered by forecho", 'caizhenghai@gmail.com'))
        self.podcast.website = self.album_url
        self.podcast.copyright = 'cc-by'
        if soup.find('div', 'album-intro') and soup.find('div', 'album-intro').get_text():
            self.podcast.description = soup.find('div', 'album-intro').get_text()
        else:
            self.podcast.description = self.podcast.name
        self.podcast.language = 'cn'
        self.podcast.image = soup.find('div', 'album-info').find('img').get('src').split('!')[0]
        self.podcast.feed_url = 'http://podcast.forecho.com/ximalaya/%s.rss' % self.album_id
        self.podcast.category = Category('Technology', 'Podcasting')
        self.podcast.explicit = False
        self.podcast.complete = False
        self.podcast.owner = Person("forecho", 'caizhenghai@gmail.com')

        album_list_content = requests.get(self.album_list_api, headers=self.header).content
        album_list_data = json.loads(album_list_content.decode('utf-8'))
        count = len(album_list_data['data']['tracksAudioPlay'])
        for each in album_list_data['data']['tracksAudioPlay']:
            try:
                detail_url = 'http://www.ximalaya.com/tracks/%s.json' % each['trackId']
                response = requests.get(detail_url, headers=self.header)
                item = json.loads(response.content)

                episode = self.podcast.add_episode()
                episode.id = str(each['index'])
                episode.title = each['trackName']
                print(self.podcast.name + '=====' + each['trackName'])
                image = each['trackCoverPath'].split('!')[0]
                if (image[-4:] == '.gif' or image[-4:] == '.bmp'):
                    episode.image = self.podcast.image
                else:
                    episode.image = image
                if item['intro']:
                    episode.summary = item['intro'].replace('\r\n', '')
                else:
                    episode.summary = each['trackName']
                episode.link = 'http://www.ximalaya.com%s' % each['albumUrl']
                episode.authors = [Person("forecho", 'caizhenghai@gmail.com')]
                episode.publication_date = self.reduction_time(item['time_until_now'], item['formatted_created_at'])
                episode.media = Media(each['src'], each['duration'])
                episode.position = count - each['index'] + 1
            except Exception as e:
                print('异常:', e)
                print('异常 URL:', 'http://www.ximalaya.com%s' % each['trackUrl'])
                traceback.print_exc()
            
        # 生成文件
        # print self.podcast.rss_str()
        self.podcast.rss_file('ximalaya/%s.rss' % self.album_id, minimize=True)

    # 时间转换 第一个参数是  "3年前", "12月11日 17:00"
    @staticmethod
    def reduction_time(time_until_now, created_at):
        date = datetime.strptime(created_at, "%m月%d日 %H:%M")
        reduction_year = datetime.now().year
        if '年前' in time_until_now:
            year = int(time_until_now.split('年前')[0])
            reduction = (datetime.now(tzlocal()) - relativedelta(years=year))
            if humanize_time(reduction) != ('%s years' % year):
                reduction_year = (datetime.now(tzlocal()) - relativedelta(years=year + 1)).year
            else:
                reduction_year = reduction.year
        elif '月前' in time_until_now:
            month = int(time_until_now.split('月前')[0])
            reduction_year = (datetime.now(tzlocal()) - relativedelta(months=month)).year
        elif '天前' in time_until_now:
            day = int(time_until_now.split('天前')[0])
            reduction_year = (datetime.now(tzlocal()) - relativedelta(days=day)).year

        return datetime(reduction_year, date.month, date.day, date.hour, date.second, tzinfo=pytz.utc)
