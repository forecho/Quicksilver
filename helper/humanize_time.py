# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import relativedelta
from dateutil.tz import tzutc, tzlocal
from twisted.trial import unittest


def humanize_time(time):
    '''
    get a datetime object and return a relative time string like
    "one hour ago", "yesterday", "3 months ago", "just now", etc.
    '''

    rd = relativedelta.relativedelta(datetime.now(tzutc()), time)

    def line(number, unit):
        if abs(number) < 10 and unit == "seconds":
            return "just now"
        if number == 1 and unit == "days":
            return 'yesterday'
        if number == -1 and unit == "days":
            return "tomorrow"

        prefix, suffix = '', ''
        unit = unit if abs(number) > 1 else unit[:-1]  # Unpluralizing.

        if number > 0:
            suffix = " ago"
        else:
            prefix = "in "

        return "%s%d %s%s" % (prefix, abs(number), unit, suffix)

    for attr in ['years', 'months', 'days', 'hours', 'minutes', 'seconds']:
        value = getattr(rd, attr)
        if value != 0:
            return line(value, attr)

    return "just now"


class UtilsTest(unittest.TestCase):
    def test_humanize_time(self):
        now = time = datetime.now(tzlocal())
        self.assertEqual('just now', humanize_time(time))

        time = now - timedelta(seconds=45)
        self.assertEqual('45 seconds ago', humanize_time(time))

        time = now - timedelta(seconds=60)
        self.assertEqual('1 minute ago', humanize_time(time))

        time = now - timedelta(seconds=15 * 60)
        self.assertEqual('15 minutes ago', humanize_time(time))

        time = now - timedelta(hours=1)
        self.assertEqual('1 hour ago', humanize_time(time))

        time = now - timedelta(hours=10)
        self.assertEqual('10 hours ago', humanize_time(time))

        time = now - timedelta(days=1)
        self.assertEqual('yesterday', humanize_time(time))

        time = now - timedelta(days=2)
        self.assertEqual('2 days ago', humanize_time(time))

        time = now - timedelta(days=31)
        self.assertEqual('1 month ago', humanize_time(time))

        time = now - timedelta(days=31 * 2)
        self.assertEqual('2 months ago', humanize_time(time))

        time = now - timedelta(days=366)
        self.assertEqual('1 year ago', humanize_time(time))

        time = now - timedelta(days=366 * 2)
        self.assertEqual('2 years ago', humanize_time(time))


if __name__ == '__main__':
    UtilsTest.test_humanize_time()
