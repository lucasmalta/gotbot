#!/home/lucas/anaconda2/bin/pytho
"""
Slack Command class: defines the action for each event

"""

import re

class Command(object):
    def __init__(self):
        self.commands = { 
            "home" : self.home,
            "food" : self.food,
            "help" : self.help
        }
        self.ammount = {'current': 0, 'food':0, 'home':0}
 
    def handle_command(self, user, command):
        response = "<@" + user + ">: "
        
        if ('food' in command) or ('ate' in command):
            if re.search('\d+', command):
              self.ammount['current'] = float( re.search('\d+', command).group() )
              self.ammount['food'] += self.ammount['current']
              response += self.commands['food']()
            else:
              response += "Sorry, you need to provide a quantity."
        
        elif ('home' in command) or ('house' in command):
            if re.search('\d+', command):
              self.ammount['current'] = float( re.search('\d+', command).group() )
              self.ammount['home'] += self.ammount['current']
              response += self.commands['home']()
            else:
              response += "Sorry, you need to provide a quantity."
             
        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()
        return response

    def food(self):
        return "OK! Adding " + str(self.ammount['current']) + " in food. Now total in: " + str(self.ammount['food'])
         
    def home(self):
        return "OK! Adding " + str(self.ammount['current']) + " in home. Now total in: " + str(self.ammount['home'])
     
    def help(self):
        response = "Currently I support the following commands:\r\n"
         
        for command in self.commands:
            response += command + "\r\n"
             
        return response

