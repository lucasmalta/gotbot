#!/home/lucas/anaconda2/bin/python
"""
Unit testing module
Test procedure

"""

import unittest
import command
import shopframe
import pandas as pd

##############################
#  COMMAND TEST PROCEDURE    #
##############################

# Create test data
file_csv = '~/GIT/gotbot/test.csv'
data = [['lucas', 20180707, 0,0], ['lucas', 20180607, 10,0]]
df = pd.DataFrame(data, columns = ['user', 'date', 'food', 'home'])
df.to_csv(file_csv, index_label=False)
channel = 'CBTCHEDGE'
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
        self.assertEqual(myCom.handle_command('luc','house', channel), '<@luc>: Sorry, you need to provide a quantity.')
    
    def test_f_total(self):
        """ Total """
        self.assertEqual(myCom.handle_command('luc','total', channel), '<@luc>: \nGrand total (*ALL DATA*):\nfood    30\nhome    15\n')
    
    def test_g_total_july(self):
        """ Total july """
        self.assertEqual(myCom.handle_command('luc','total july', channel), '<@luc>: \nTotal for *July*, *2018*\nfood    20\nhome    15\n')
    
    def test_h_total_june(self):
        """ Total june """
        self.assertEqual(myCom.handle_command('luc','total june', channel), '<@luc>: \nTotal for *June*, *2018*\nfood    10\nhome     0\n')
    
    def test_i_total_june2(self):
        """ Total june 06/2018 """
        self.assertEqual(myCom.handle_command('luc','total 06/2018', channel), '<@luc>: \nTotal for *June*, *2018*\nfood    10\nhome     0\n')
    def test_j_total_june3(self):
        """ Total june 06/18 """
        self.assertEqual(myCom.handle_command('luc','total 06/18', channel), '<@luc>: \nTotal for *June*, *2018*\nfood    10\nhome     0\n')
    
    def test_k_total_may(self):
        """ Total may 18 """
        self.assertEqual(myCom.handle_command('luc','total may 18', channel), '<@luc>: \nTotal for *May*, *2018*\nfood    0.0\nhome    0.0\n')






##############################
#  SHOPFRAME TEST PROCEDURE  #
##############################

# Create test data
file_csv = '~/GIT/gotbot/test.csv'
data = ['lucas', 20180707, 0,0]
df = pd.DataFrame([data], columns = ['user', 'date', 'food', 'home'])
df.to_csv(file_csv, index_label=False)

# Read test data
myshop = shopframe.ShopFrame(file_csv)  

class AddPoint(unittest.TestCase):
    """ Test case for shopframe.py -- Adding data """
  
    def test_a_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('lucas','food', 20180705, 10),0)

    def test_b__get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], 10)
    
    def test_c_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['home'], 0)
    
    def test_d_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('lucas','home', 20180705, 25),0)
    
    def test_e_get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], 10)
    
    def test_f_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['home'], 25)

    def test_g_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('lucas','food', 20180705, 10),0)
    
    def test_h_get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], 20)
    
    def test_i_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['home'], 25)

    def test_j_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('lucas','food', 20180705, -30),0)
    
    def test_k_get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['food'], -10)
    
    def test_l_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['home'], 25)





if __name__ == '__main__':
    unittest.main()



