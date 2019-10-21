# !/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time
import traceback

from spider.qingting import Qingting
from spider.ximalaya import Ximalaya


# reload(sys)
# sys.setdefaultencoding("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("channel", help=u"渠道(现只有喜马拉雅和蜻蜓fm)", choices=['ximalaya', 'qingting'])
    parser.add_argument("id", help=u"对应渠道下的专辑id")
    args = parser.parse_args()
    log = open("error.log", "a")
    for album_id in args.id.split(','):
        lookup = {'qingting': Qingting(album_id), 'ximalaya': Ximalaya(album_id)}
        try:
            my_instance = lookup.get(args.channel)
            my_instance.album()
        except Exception as e:
            print('异常:', e)
            traceback.print_exc()
            curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            log.write("{}：爬取{}的{}失败：{}\n".format(curr_time, args.channel, str(album_id), str(e)))


main()
