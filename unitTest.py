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
data = ['lucas', 20180707, 0,0]
df = pd.DataFrame([data], columns = ['user', 'date', 'food', 'home'])
df.to_csv(file_csv, index_label=False)
channel = 'CBTCHEDGE'
myCom = command.Command(file_csv)

class AddCommand(unittest.TestCase):
    """ Test case for command.py -- Adding data """
  
    def test_a_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','food 5', channel), '<@luc>: OK! Adding 5 in food. New total is: 5')
    
    def test_b_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','food 15', channel), '<@luc>: OK! Adding 15 in food. New total is: 20')
    
    def test_c_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','house 15', channel), '<@luc>: OK! Adding 15 in home. New total is: 15')
    
    def test_d_add_comm(self):
        """ Test add point """
        self.assertEqual(myCom.handle_command('luc','house 0', channel), '<@luc>: OK! Adding 0 in home. New total is: 15')

    def test_e_total(self):
        """ Total """
        self.assertEqual(myCom.handle_command('luc','total', channel), '<@luc>: \nfood    20\nhome    15\n')






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



