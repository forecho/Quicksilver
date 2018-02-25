# !/usr/bin/env python
# -*- coding: utf-8 -*-
from spider.ximalaya import Ximalaya
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    album_ids = sys.argv[1]  # get token from command-line
    # print album_ids.split(',')
    for album_id in album_ids.split(','):
        Ximalaya(album_id).album()

main()
