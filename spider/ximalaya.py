# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import math
import traceback
from datetime import datetime

import pytz
import requests
import hashlib
import random
import time
from podgen import Media, Podcast, Person, Category


class Ximalaya():
    def __init__(self, album_id):
        self.podcast = None
        self.album_id = album_id
        self.page_size = 30
        self.album_info_url = "https://www.ximalaya.com/revision/album?albumId={}"
        self.album_list_url = "https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&pageSize={}"
        self.detail_url = "https://mobile.ximalaya.com/v1/track/baseInfo?device=android&trackId={}"
        self.album_url = "https://www.ximalaya.com/album/{}"
        self.time_api = 'https://www.ximalaya.com/revision/time'
        self.s = requests.session()
        self.header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self.album_url.format(self.album_id),
            'Cookie': '_ga=GA1.2.1628478964.1476015684; _gat=1',
            'Host': 'www.ximalaya.com'
        }

    def album(self):
        self.get_sign()
        album_info = self.s.get(self.album_info_url.format(self.album_id), headers=self.header).content
        album_info_content = json.loads(album_info.decode('utf-8'))
        if album_info_content['ret'] == 200:
            album_info_data = album_info_content['data']

            # 初始化
            self.podcast = Podcast()
            self.podcast.name = album_info_data['mainInfo']['albumTitle']
            self.podcast.authors.append(Person("Powered by forecho", 'caizhenghai@gmail.com'))
            self.podcast.website = self.album_url.format(self.album_id)
            self.podcast.copyright = 'cc-by'
            if album_info_data['mainInfo']['richIntro']:
                self.podcast.description = album_info_data['mainInfo']['richIntro']
            else:
                self.podcast.description = self.podcast.name
            self.podcast.language = 'cn'
            self.podcast.image = 'https:' + album_info_data['mainInfo']['cover'].split('!')[0]
            self.podcast.feed_url = 'http://podcast.forecho.com/ximalaya/%s.rss' % self.album_id
            self.podcast.category = Category('Technology', 'Podcasting')
            self.podcast.explicit = False
            self.podcast.complete = False
            self.podcast.owner = Person("forecho", 'caizhenghai@gmail.com')
            page_num = 1
            # py2 +1
            track_total_count = math.ceil(album_info_data['tracksInfo']['trackTotalCount'] / self.page_size) + 1
            while page_num <= track_total_count:
                album_list = self.s.get(self.album_list_url.format(self.album_id, page_num, self.page_size),
                                          headers=self.header).content
                album_list_content = json.loads(album_list.decode('utf-8'))
                count = len(album_list_content['data']['tracksAudioPlay'])
                for each in album_list_content['data']['tracksAudioPlay']:
                    try:
                        print(self.detail_url.format(each['trackId']))
                        detail = self.s.get(self.detail_url.format(each['trackId']), headers=self.header).content
                        detail_content = json.loads(detail.decode('utf-8'))
                        episode = self.podcast.add_episode()
                        episode.id = str(each['index'])
                        episode.title = each['trackName']
                        print(self.podcast.name + '=====' + each['trackName'])
                        image = each['trackCoverPath'].split('!')[0]
                        if image[-4:] == '.png' or image[-4:] == '.jpg':
                            episode.image = 'https:' + image
                        else:
                            episode.image = self.podcast.image
                        if 'intro' in detail_content:
                            episode.summary = detail_content['intro'].replace('\r\n', '')
                        else:
                            episode.summary = each['trackName']
                        episode.link = 'http://www.ximalaya.com%s' % each['albumUrl']
                        episode.authors = [Person("forecho", 'caizhenghai@gmail.com')]
                        episode.publication_date = self.reduction_time(detail_content['createdAt'])
                        episode.media = Media(each['src'], each['duration'])
                        episode.position = count - each['index'] + 1
                    except Exception as e:
                        print('异常:', e)
                        print('异常 URL:', 'https://www.ximalaya.com%s' % each['trackUrl'])
                        traceback.print_exc()
                # 生成文件
                # print self.podcast.rss_str()
                page_num = page_num + 1
            self.podcast.rss_file('ximalaya/%s.rss' % self.album_id, minimize=True)

    def get_time(self):
        """
        获取服务器时间戳
        :return:
        """
        r = self.s.get(self.time_api, headers=self.header)
        return r.text

    def get_sign(self):
        """
        获取sign： md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :return: xm_sign
        """
        now_time = str(round(time.time() * 1000))
        server_time = self.get_time()
        sign = str(hashlib.md5("himalaya-{}".format(server_time).encode()).hexdigest()) + "({})".format(
            str(round(random.random() * 100))) + server_time + "({})".format(str(round(random.random() * 100))) + now_time
        self.header["xm-sign"] = sign
        # print(sign)
        # return sign

    # 时间转换 参数 毫秒时间戳
    @staticmethod
    def reduction_time(time):
        timestamp = datetime.fromtimestamp(time / 1000)
        return datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute,
                        tzinfo=pytz.utc)
