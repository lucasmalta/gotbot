#!/usr/bin/env python
"""
Unit testing module
Test procedure

"""

import unittest
import command
import shopframe
import pandas as pd
import datetime
from approvaltests.approvals import verify
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
from mock import MagicMock

# Save a couple of test days
mock_today = datetime.datetime(year=2018, month=7, day=15)

# Mock datetime to control today's date
datetime = MagicMock()
datetime.date.today.return_value = mock_today


# Create test data
file_csv = '~/GIT/gotbot/test.csv'
data = [['luc', 'home 0', 20180707, '_P', 0,0], ['ana', 'food 10',20180607, '_P', 10,0]]
df = pd.DataFrame(data, columns = ['user', 'comm', 'date', 'tags', 'food', 'home'])
df.to_csv(file_csv, index_label=False)
channel = 'CBTCHEDGE'
timenow = datetime.date.today()
monthnow = timenow.strftime("%B")
yearnow = timenow.strftime("%Y")
daynow = str(timenow.year) + '{:02d}'.format(timenow.month) + '{:02d}'.format(timenow.day)
myCom = command.Command(file_csv, timenow)


printerFun = myCom.handle_command('luc','food 5', channel) + '\n' + \
           myCom.handle_command('luc','food 15', channel)  + '\n' + \
           myCom.handle_command('luc','house 15', channel) + '\n' + \
           myCom.handle_command('luc','house 0', channel)  + '\n' + \
           myCom.handle_command('luc','house', channel)    + '\n' + \
           myCom.handle_command('luc','total ', channel)   + '\n' + \
           myCom.handle_command('luc','total ' + monthnow + yearnow, channel) + '\n' + \
           myCom.handle_command('luc','total june' + yearnow, channel) + '\n' + \
           myCom.handle_command('luc','total 06/2018', channel) + '\n' + \
           myCom.handle_command('luc','total may 2018', channel) + '\n' + \
           myCom.handle_command('ana','total me June ' + yearnow, channel) + '\n' + \
           myCom.handle_command('luc','total me june 2018', channel) + '\n' + \
           myCom.handle_command('ana','total me ' + monthnow + yearnow, channel) + '\n' + \
           myCom.handle_command('luc','total me' + monthnow + yearnow, channel) + '\n' + \
           myCom.handle_command('ana','show paid', channel) + '\n' + \
           myCom.handle_command('ana','food 15', channel) + '\n' + \
           myCom.handle_command('ana','from paid', channel)

class GettingStartedTest(unittest.TestCase):
    def setUp(self):
        self.reporter = GenericDiffReporterFactory().get_first_working()

    def test_simple(self):
        verify(printerFun, self.reporter)


if __name__ == "__main__":
    unittest.main()

