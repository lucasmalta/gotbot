#!/home/lucas/anaconda2/bin/pytho
"""
Slack Command class: defines the action for each event

"""

import re
import shopframe
import datetime

class Command(object):
    """ Class for commands"""
    def __init__(self):
        """ Constructor """
        self.commands = { 
            "food" : self.food,
            "help" : self.help
        }
        self.file_csv = '~/GIT/gotbot/luc.csv'
        self.myshop = shopframe.ShopFrame(self.file_csv)
 
    def handle_command(self, user, command):
        """ Parse command text """
        response = "<@" + user + ">: "
        
        if ('food' in command) or ('ate' in command):
            if re.search(r'[+-]*\d+', command) is not None:
                ammount = int(re.search(r'[+-]*\d+', command).group())
                response += self.commands['food'](user, ammount)
            else:
                response += "Sorry, you need to provide a quantity."
        
             
        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()
        return response


    def food(self, user, ammount):
        """ What do do when food-related keywords are found within command """
        date = datetime.datetime.today().strftime('%Y%m%d')
        # Add amount to DataFrame
        try:
            self.myshop.add_data_point(user,'Food', date, ammount)
            new_total = self.myshop.get_grand_total()
        except:
            print "Error adding value to DF"
        else:
            return "OK! Adding {} in food. New total is: {}".format(ammount, new_total['Food'])
         
     
    def help(self):
        """ What do do when help keyword is found within command """
        response = "Currently I support the following commands:\r\n"
         
        for command in self.commands:
            response += command + "\r\n"
             
        return response

