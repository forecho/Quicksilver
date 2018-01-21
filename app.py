# !/usr/bin/env python
# -*- coding: utf-8 -*-
from spider.ximalaya import Ximalaya
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    album_id = sys.argv[1]  # get token from command-line
    Ximalaya(album_id).album()


main()