# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime

import pytz
import requests
from podgen import Media, Podcast, Person, Category


class Qingting(object):
    def __init__(self, album_id):
        self.podcast = None
        self.album_id = album_id
        self.url = 'http://www.qingting.fm/channels/{}'.format(album_id)
        self.album_list_api = "http://api2.qingting.fm/v6/media/channelondemands/{}/programs/order/0/curpage/1/pagesize/999".format(
            album_id)
        self.album_info_api = "http://api2.qingting.fm/v6/media/channelondemands/{}".format(album_id)

    def album(self):
        album_info_content = requests.get(self.album_info_api).content
        album_info_data = json.loads(album_info_content.decode('utf-8'))
        album_list_content = requests.get(self.album_list_api).content
        album_list_data = json.loads(album_list_content.decode('utf-8'))

        self.podcast = Podcast()
        self.podcast.name = album_info_data['data']['title']
        self.podcast.authors.append(Person("Powered by maijver", 'maijver@gmail.com'))
        self.podcast.website = self.url
        self.podcast.copyright = 'cc-by'
        self.podcast.description = album_info_data['data']['description']
        self.podcast.language = 'cn'
        self.podcast.image = album_info_data['data']['thumbs']['small_thumb'].replace('!200', '')
        self.podcast.feed_url = 'http://podcast.forecho.com/qingting/%s.rss' % self.album_id
        self.podcast.category = Category('Technology', 'Podcasting')
        self.podcast.explicit = False
        self.podcast.complete = False
        self.podcast.owner = Person("maijver", 'maijver@gmail.com')

        for each in album_list_data['data']:
            episode = self.podcast.add_episode()
            episode.id = str(each['id'])
            episode.title = each['title']
            print(self.podcast.name + '=====' + each['title'])
            episode.image = album_info_data['data']['thumbs']['small_thumb'].replace('!200', '')
            episode.summary = each['title']
            episode.link = 'http://www.qingting.fm/channels/{}/programs/{}'.format(self.album_id, each['id'])
            episode.authors = [Person("forecho", 'caizhenghai@gmail.com')]
            episode.publication_date = self.reduction_time(each['update_time'])
            episode.media = Media("http://od.qingting.fm/{}".format(each['mediainfo']['bitrates_url'][0]['file_path']),
                                  each['duration'])

        self.podcast.rss_file('qingting/{}.rss'.format(self.album_id), minimize=True)

    @staticmethod
    def reduction_time(created_date):
        timestamp = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
        return datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute,
                        tzinfo=pytz.utc)
