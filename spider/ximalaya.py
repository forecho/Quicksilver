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
        self.url = 'http://www.ximalaya.com/album/%s' % album_id
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

        #find zhubo id
        zhubo_id = soup.find('div', 'picture').a['href'][7:-1]

        #create url with zhubo id
        new_url = self.url[0:24] + zhubo_id + '/' + self.url[24:]

        #find the page count
        albumsoundcount = int(soup.find('span', 'albumSoundcount').get_text()[1:-1])
        pagecount_full = albumsoundcount/100
        if ( albumsoundcount%100 == 0 ):
            pagecount = pagecount_full
        else:
            pagecount = pagecount_full + 1

        # get all pages and soups
        page_list = []
        soup_list = []
        count = 1
        while (count <= pagecount):
            page_list.append(requests.get(new_url + '?page=' + '%d'%count, headers=self.header))
            soup_list.append(BeautifulSoup(page_list[count-1].content, "lxml"))
            count = count + 1

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

        #sound_ids on all pages
        sound_ids_list = []
        for item in soup_list:
            sound_ids_list.append(item.find('div', class_='personal_body').get('sound_ids').split(','))

        count = 1
        while (count <= pagecount):
            for sound_id in sound_ids_list[count-1]:
                date = soup_list[count-1].find('li', sound_id=sound_id).find('div', class_='operate').get_text().strip()
                self.detail(sound_id, date)
            count = count + 1

        # 生成文件
        # print self.podcast.rss_str()
        self.podcast.rss_file('ximalaya/%s.rss' % self.album_id, minimize=True)

    def detail(self, sound_id, date):
        detail_url = 'http://www.ximalaya.com/tracks/%s.json' % sound_id
        response = requests.get(detail_url, headers=self.header)
        item = json.loads(response.content)

        episode = self.podcast.add_episode()
        episode.id = str(item['id'])
        episode.title = item['title']
        image = item['cover_url_142'].split('?')[0]
        if (image[-4:] == '.gif'):
            episode.image = self.podcast.image
        else:
            episode.image = image
        episode.summary = (item['intro'].replace('\n', '') if item['intro'] else '')
        episode.link = 'http://www.ximalaya.com/sound/%d' % item['id']
        episode.authors = [Person("forecho", 'caizhenghai@gmail.com')]
        episode.publication_date = self.reduction_time(
            date, item['formatted_created_at'])
        episode.media = Media(item['play_path_64'], 454599964)
        # 坑爹的 Windows CMD https://www.v2ex.com/t/98936
        print self.podcast.name + '=====' + item['title'].encode('gbk', 'ignore').decode('gbk')

    # 时间转换 第一个参数是年月日 第二个参数"12月11日 17:00"
    @staticmethod
    def reduction_time(date, created_date):
        timestamp = datetime.strptime(date, "%Y-%m-%d")
        created_at = datetime.strptime(created_date.split(' ')[1], "%H:%M")
        return datetime(timestamp.year, timestamp.month, timestamp.day, created_at.hour, created_at.minute,
                        tzinfo=pytz.utc)