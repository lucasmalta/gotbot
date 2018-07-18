#!/home/lucas/anaconda2/bin/python
"""
Unit testing module
Command test procedure

"""

import unittest
import command


myCom = command.Command()  

class FoodTestCase(unittest.TestCase):
    """ Test case for command.py """
  
    def test_food_reply(self):
        """ Test food """
        self.assertEqual(myCom.handle_command('luc','food 10'), '<@luc>: OK! Adding 10 in food. New total is: 10')
    
    def test_no_ammount_food_reply(self):
        """ Test food without specifying amomunt """
        self.assertEqual(myCom.handle_command('luc','food'), '<@luc>: Sorry, you need to provide a quantity.')

    def test_neg_ammount_food_reply(self):
        """ Test food with negative amomunt """
        self.assertEqual(myCom.handle_command('luc','food -10'), '<@luc>: OK! Adding -10 in food. New total is: 0')



class HomeTestCase(unittest.TestCase):
    """ Test case for command.py """
  
    def test_home_reply(self):
        """ Test home """
        self.assertEqual(myCom.handle_command('luc','home 10'), '<@luc>: OK! Adding 10 in home. New total is: 10')

    def test_no_ammount_home_reply(self):
        """ Test home without specifying amomunt """
        self.assertEqual(myCom.handle_command('luc','home'), '<@luc>: Sorry, you need to provide a quantity.')

    def test_neg_ammount_home_reply(self):
        """ Test home with negative amomunt """
        self.assertEqual(myCom.handle_command('luc','home -10'), '<@luc>: OK! Adding -10 in home. New total is: 0')



class TotalTestCase(unittest.TestCase):
    """ Test case for command.py """
  
    def test_total_reply(self):
        """ Test total """
        self.assertEqual(myCom.handle_command('luc','total'), '<@luc>: Right. The total so far is: \n Food: 0 \n Home: 0')






if __name__ == '__main__':
    unittest.main()



