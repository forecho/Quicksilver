# !/usr/bin/env python
# -*- coding: utf-8 -*-
from spider.ximalaya import Ximalaya
from spider.qingting import Qingting
import sys
import argparse

reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("channel", help=u"渠道(现只有喜马拉雅和蜻蜓fm)", choices=['ximalaya', 'qingting'])
    parser.add_argument("id", help=u"对应渠道下的专辑id")
    args = parser.parse_args()
    for album_id in args.id.split(','):
        lookup = {'qingting': Qingting(album_id), 'ximalaya': Ximalaya(album_id)}
        myinstance = lookup.get(args.channel)
        myinstance.album()


main()
