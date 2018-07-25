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

#myCom = command.Command()


##############################
#  SHOPFRAME TEST PROCEDURE  #
##############################

# Create test data
file_csv = '~/GIT/gotbot/test.csv'
data = ['Lucas', 20180707, 0,0]
df = pd.DataFrame([data], columns = ['User', 'Date', 'Food', 'Home'])
df.to_csv(file_csv, index_label=False)

# Read test data
myshop = shopframe.ShopFrame(file_csv)  

class AddPoint(unittest.TestCase):
    """ Test case for shopframe.py -- Adding data """
  
    def test_a_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('Lucas','Food', 20180705, 10),0)

    def test_b__get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['Food'], 10)
    
    def test_c_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['Home'], 0)
    
    def test_d_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('Lucas','Home', 20180705, 25),0)
    
    def test_e_get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['Food'], 10)
    
    def test_f_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['Home'], 25)

    def test_g_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('Lucas','Food', 20180705, 10),0)
    
    def test_h_get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['Food'], 20)
    
    def test_i_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['Home'], 25)

    def test_j_add_point(self):
        """ Test add point """
        self.assertEqual(myshop.add_data_point('Lucas','Food', 20180705, -30),0)
    
    def test_k_get_grand_total_food(self):
        """ Test total for food """
        t = myshop.get_grand_total()
        self.assertEqual(t['Food'], -10)
    
    def test_l_get_grand_total_home(self):
        """ Test total for home """
        t = myshop.get_grand_total()
        self.assertEqual(t['Home'], 25)





if __name__ == '__main__':
    unittest.main()



