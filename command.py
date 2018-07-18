#!/home/lucas/anaconda2/bin/pytho
"""
Slack Command class: defines the action for each event

"""

import re

class Command(object):
    """ Class for commands"""
    def __init__(self):
        """ Constructor """
        self.commands = { 
            "home" : self.home,
            "food" : self.food,
            "total" : self.total,
            "help" : self.help
        }
        self.ammount = {'current': 0, 'food':0, 'home':0}
 
    def handle_command(self, user, command):
        """ Parse command text """
        response = "<@" + user + ">: "
        
        if ('food' in command) or ('ate' in command):
            if re.search(r'\d+', command):
                self.ammount['current'] = float(re.search(r'\d+', command).group())
                self.ammount['food'] += self.ammount['current']
                response += self.commands['food']()
            else:
                response += "Sorry, you need to provide a quantity."
        
        elif ('home' in command) or ('house' in command):
            if re.search(r'\d+', command):
                self.ammount['current'] = float(re.search(r'\d+', command).group())
                self.ammount['home'] += self.ammount['current']
                response += self.commands['home']()
            else:
                response += "Sorry, you need to provide a quantity."
        
        elif 'total' in command:
            response += self.commands['total']()
             
        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()
        return response

    def food(self):
        """ What do do when food-related keywords are found within command """
        return "OK! Adding {} in food. New total is: {}"\
        .format(self.ammount['current'], self.ammount['food'])
         
    def home(self):
        """ What do do when home-related keywords are found within command """
        return "OK! Adding {} in home. New total is: {}"\
        .format(self.ammount['current'], self.ammount['home'])
    
    def total(self):
        """ What do do when total keyword is found within command """
        return "Right. The total so far is: \n Food: {} \n Home: {}".\
        format(self.ammount['food'], self.ammount['home'])
     
    def help(self):
        """ What do do when help keyword is found within command """
        response = "Currently I support the following commands:\r\n"
         
        for command in self.commands:
            response += command + "\r\n"
             
        return response

