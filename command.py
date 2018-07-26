#!/home/lucas/anaconda2/bin/pytho
"""
Slack Command class: defines the action for each event

"""

import re
import datetime
import matplotlib.pyplot as plt
import os
import commands
import sys
import shopframe


class Command(object):
    """ Class for commands"""
    def __init__(self, *argv):
        """ Constructor """
        self.commands = { 
            "add_amount" : self.add_amount,
            "grand_total" : self.grand_total,
            "plot" : self.plot,
            "help" : self.help
        }
        self.root_folder = '/home/lucas/GIT/gotbot/'
        if argv:
            self.file_csv = argv[0]
        else:
            self.file_csv = self.root_folder + 'gotbot.csv'
        self.myshop = shopframe.ShopFrame(self.file_csv)
 
    def handle_command(self, user, command, channel):
        """ Parse command text """
        response = "<@" + user + ">: "
        command = command.lower()
 
        # Parse for different categories       
        # FOOD - GENERAL
        if ('food' in command) or ('super' in command) or ('supermarket' in command)\
           or ('groceries' in command):
            response += self.add_amount(user, command, 'food')
        elif ('home' in command) or ('house' in command) or ('casa' in command):
            response += self.add_amount(user, command, 'home')
        elif ('travel' in command) or ('trip' in command) or ('hotel' in command) or\
           ('ticket' in command):
            response += self.add_amount(user, command, 'travel')
        elif ('bar' in command) or ('restaurant' in command):
            response += self.add_amount(user, command, 'bar')
        elif ('misc' in command) or ('other' in command):
            response += self.add_amount(user, command, 'misc')
        elif ('total' in command) or ('tot' in command):
            response += self.grand_total()
        elif ('plot' in command) or ('plt' in command):
            response += self.plot(channel)

        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()
        return response 


    def add_amount(self, user, command, typex):
        """ What do do when keywords are found within command """
        if re.search(r'[+-]*\d+', command) is not None:
            amount = int(re.search(r'[+-]*\d+', command).group())
        else:
            return "Sorry, you need to provide a quantity."
        date = datetime.datetime.today().strftime('%Y%m%d')
        # Add amount to DataFrame
        try:
            self.myshop.add_data_point(user, typex, date, amount)
            new_total = self.myshop.get_grand_total()
        except ValueError:
            print "Error adding value to DF"
        else:
            return "OK! Adding {} in {}. New total is: {}".format(amount, typex, new_total[typex])
    
    def grand_total(self):
        """ What do do when keyword "total" is found within command """
        total = self.myshop.get_grand_total()
        return '\n' + str(total).split('dtype')[0]
    
    def plot(self, channel):
        """ Plotting capability """
        total = self.myshop.get_grand_total()
        D = total.to_dict()
        plt.bar(range(len(D)), D.values(), align='center', color='black')
        plt.xticks(range(len(D)), list(D.keys()))
        plt.ylabel('SEK',fontsize=11)
        plt.xlabel('Category',fontsize=11)
        plt.savefig('imgs/foo.png')
        verif_token = os.getenv('MYTOKEN')
        cmd = 'curl -F file=@' + self.root_folder + 'imgs/foo.png -F \
        channels=' + channel + ' -H "Authorization: Bearer ' + verif_token + '" \
        https://slack.com/api/files.upload'
        (status, output) = commands.getstatusoutput(cmd)
        match = re.search(r'"ok":(\w+),',output)
        if match:
            if 'true' not in match.group(1): 
                return 'Could not plot, sorry'
        else: return 'Could not plot, sorry'
        return 'Done.'

 
    def help(self):
        """ What do do when help keyword is found within command """
        response = "Currently I support the following commands:\r\n"
         
        for command in self.commands:
            response += command + "\r\n"
             
        return response

