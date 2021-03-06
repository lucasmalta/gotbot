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

##############################
#  COMMAND TEST PROCEDURE    #
##############################

# Create test data
file_csv = '~/GIT/gotbot/test.csv'
data = [['luc', 'home 0', 20180707, '_P', 0,0], ['ana', 'food 10',20180607, '', 10,0]]
df = pd.DataFrame(data, columns = ['user', 'comm', 'date', 'tags', 'food', 'home'])
df.to_csv(file_csv, index_label=False)
channel = 'CBTCHEDGE'
timenow = datetime.date.today()
monthnow = timenow.strftime("%B")
daynow = str(timenow.year) + '{:02d}'.format(timenow.month) + '{:02d}'.format(timenow.day)
myCom = command.Command(file_csv)

class AddCommand(unittest.TestCase):
    """ Test case for command.py -- Adding data """
  
    def test_a_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','food 5', channel), '<@luc>: OK! Adding 5 in food.')
    
    def test_b_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','food 15', channel), '<@luc>: OK! Adding 15 in food.')
    
    def test_c_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','house 15', channel), '<@luc>: OK! Adding 15 in home.')
    
    def test_d_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','house 0', channel), '<@luc>: OK! Adding 0 in home.')

    def test_e_add_comm(self):
        """ Test empty """
        self.assertEqual(myCom.handle_command('luc','house', channel),\
       '<@luc>: Sorry, you need to provide a quantity.')
    
    def test_f_total(self):
        """ Total """
        self.assertEqual(myCom.handle_command('luc','total', channel),\
        '<@luc>: \nGrand total (*ALL DATA*):\nfood    30\nhome    15\n')
    
    def test_g_total_current(self):
        """ Total current month """
        self.assertEqual(myCom.handle_command('luc','total ' + monthnow, channel),\
        '<@luc>: \nTotal for *' + monthnow + '*, *2018*\nfood    20\nhome    15\n')
    
    def test_h_total_june(self):
        """ Total june """
        self.assertEqual(myCom.handle_command('luc','total june', channel),\
        '<@luc>: \nTotal for *June*, *2018*\nfood    10\nhome     0\n')
    
    def test_i_total_june2(self):
        """ Total june 06/2018 """
        self.assertEqual(myCom.handle_command('luc','total 06/2018', channel),\
        '<@luc>: \nTotal for *June*, *2018*\nfood    10\nhome     0\n')
    
    def test_j_total_june3(self):
        """ Total june 06/18 """
        self.assertEqual(myCom.handle_command('luc','total 06/18', channel),\
        '<@luc>: \nTotal for *June*, *2018*\nfood    10\nhome     0\n')
    
    def test_k_total_may(self):
        """ Total may 18 """
        self.assertEqual(myCom.handle_command('luc','total may 18', channel),\
        '<@luc>: \nTotal for *May*, *2018*\nfood    0.0\nhome    0.0\n')

    def test_l_total_me_june(self):
        """ Total me June """
        self.assertEqual(myCom.handle_command('ana','total me June', channel),\
        '<@ana>: \nTotal for *June*, *2018*\nfood    10\nhome     0\n')
        self.assertEqual(myCom.handle_command('luc','total me june', channel),\
        '<@luc>: \nTotal for *June*, *2018*\nfood    0.0\nhome    0.0\n')
    
    def test_m_total_me_current(self):
        """ Total me current month """
        self.assertEqual(myCom.handle_command('ana','total me ' + monthnow, channel),\
        '<@ana>: \nTotal for *' + monthnow + '*, *2018*\nfood    0.0\nhome    0.0\n')
        self.assertEqual(myCom.handle_command('luc','total me ' + monthnow, channel),\
        '<@luc>: \nTotal for *' + monthnow  + '*, *2018*\nfood    20\nhome    15\n')

    def test_n_total_me(self):
        """ Total me """
        self.assertEqual(myCom.handle_command('luc','total me', channel),\
        '<@luc>: \nGrand total (*ALL DATA*):\nfood    20\nhome    15\n')
        self.assertEqual(myCom.handle_command('ana','total me', channel),\
        '<@ana>: \nGrand total (*ALL DATA*):\nfood    10\nhome     0\n')

    def test_o_show_paid(self):
        """ Get paid """
        self.assertEqual(myCom.handle_command('luc','show paid', channel),\
        '<@luc>: Everything is paid until (and including): 20180707')
    
    def test_p_getset_paid(self):
        """ Get paid """
        self.assertEqual(myCom.handle_command('luc','set paid', channel),\
        '<@luc>: Setting everything to *paid*.')
        self.assertEqual(myCom.handle_command('luc','show paid', channel),\
        '<@luc>: Everything is paid until (and including): ' + daynow)
        self.assertEqual(myCom.handle_command('luc','set unpaid', channel),\
        '<@luc>: Setting everything to *unpaid*.')
        self.assertEqual(myCom.handle_command('luc','show paid', channel),\
        '<@luc>: Everything is paid until (and including): ')
    
    def test_q_show_comm(self):
        """ Get paid """
        self.assertEqual(myCom.handle_command('luc','show comm', channel),\
        '<@luc>: Entries for the *current* month:\n\n' + daynow  + '    food 5\n' + daynow  + '   food 15\n' + daynow  + '  house 15\n' + daynow  + '   house 0')


##############################
#  SHOPFRAME TEST PROCEDURE  #
##############################

# Create test data
file_csv = '~/GIT/gotbot/test.csv'
data = [['luc', 'home 0', 20180707,'_P', 0,0], ['ana', 'food 10', 20180607,'', 10,0]]
df = pd.DataFrame(data, columns = ['user', 'comm', 'date','tags', 'food', 'home'])
df.to_csv(file_csv, index_label=False)

# Read test data
myshop = shopframe.ShopFrame(file_csv)  

class AddPoint(unittest.TestCase):
    """ Test case for shopframe.py -- Adding data """
  
    def test_a_add_point(self):
        self.assertEqual(myshop.add_data_point('luc', 'food 10' ,'food', 20180705, 10),0)

    def test_b__get_grand_total(self):
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], 20)
        self.assertEqual(t['home'], 0)
    
    def test_c_add_point(self):
        self.assertEqual(myshop.add_data_point('luc', 'home 25' ,'home', 20180705, 25),0)
    
    def test_d_get_grand_total(self):
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], 20)
        self.assertEqual(t['home'], 25)

    def test_e_add_point(self):
        self.assertEqual(myshop.add_data_point('luc', 'food 10','food', 20180705, 10),0)
    
    def test_f_get_grand_total(self):
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], 30)
        self.assertEqual(t['home'], 25)

    def test_g_add_point(self):
        self.assertEqual(myshop.add_data_point('luc', 'food -20','food', 20180705, -20),0)
    
    def test_h_get_grand_total(self):
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], 10)
        self.assertEqual(t['home'], 25)

    def test_i_get_total_by_date(self):
        t = myshop.get_total_by_date(min_date='20180701', max_date='20180731')
        self.assertEqual(t['home'], 25)
        self.assertEqual(t['food'], 0)
    
    def test_j_get_total_by_date(self):
        t = myshop.get_total_by_date(min_date='20180601', max_date='20180631')
        self.assertEqual(t['home'], 0)
        self.assertEqual(t['food'], 10)
    
    def test_k_get_total_by_date_user(self):
        t = myshop.get_total_by_date(user='ana', min_date='20180601', max_date='20180631')
        self.assertEqual(t['home'], 0)
        self.assertEqual(t['food'], 10)
        
    def test_l_get_total_by_date_user(self):
        t = myshop.get_total_by_date(user='ana', min_date='20180701', max_date='20180731')
        self.assertEqual(t['home'], 0)
        self.assertEqual(t['food'], 0)
    
    def test_m_get_total_by_date_user(self):
        t = myshop.get_total_by_date(user='ana', min_date='20180601', max_date='20180731')
        self.assertEqual(t['home'], 0)
        self.assertEqual(t['food'], 10)

    def test_n_get_total_by_date_user(self):
        t = myshop.get_total_by_date(user='ana', min_date='20180601', max_date='20180731')
        self.assertEqual(t['home'], 0)
        self.assertEqual(t['food'], 10)

    def test_o_grand_total_by_user(self):
        t = myshop.get_grand_total(user='ana')
        self.assertEqual(t['home'], 0)
        self.assertEqual(t['food'], 10)
    
    def test_p_grand_total_by_user(self):
        t = myshop.get_grand_total(user='luc')
        self.assertEqual(t['home'], 25)
        self.assertEqual(t['food'], 0)

    def test_q_get_tag(self):
        t = myshop.get_tag('_P')
        self.assertEqual(t, '20180707')
    
    def test_r_set_tag(self):
        t = myshop.set_tag('_P')
        t = myshop.get_tag('_P')
        self.assertEqual(t, '20180707')
    
    def test_s_del_tag(self):
        t = myshop.del_tag('_P')
        t = myshop.get_tag('_P')
        self.assertEqual(t, '')




if __name__ == '__main__':
    unittest.main()



