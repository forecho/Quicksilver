# !/usr/bin/env python
# -*- coding: utf-8 -*-
from spider.ximalaya import Ximalaya
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    Ximalaya(12271374).album()


main()
