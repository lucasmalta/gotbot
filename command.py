"""
Slack Command class: defines the action for each event

"""
import re
import json
import datetime
import datefinder
import matplotlib.pyplot as plt
import os
import commands
import shopframe


class Command(object):
    """ Class for commands"""
    def __init__(self, *argv):
        """ Constructor """
        self.cat_file = 'categories.json'
        if argv:
            self.file_csv = argv[0]
        else:
            self.file_csv = 'gotbot.csv'
        self.myshop = shopframe.ShopFrame(self.file_csv)
        
        # Load json file with categories
        with open(self.cat_file) as catfile:   
            self.data_cat = json.load(catfile)

 
    def handle_command(self, user, command, channel):
        """ Parse command text """
        response = "<@" + user + ">: "
        command = command.lower()
 
        # Parse for different categories       
        for key, value in self.data_cat.iteritems():
            if any([x in command for x in value]):
                response += self.add_amount(user, command, key)
      
        # Parse for total
        if 'total' in command:
            arg_user = ''
            if ('me' in command) or ('my' in command):
                arg_user = user
            if ('month' in command) or ('current' in command) or ('now' in command):
                # Total for present month
                response += self.total_by_month(mydate = datetime.date.today(),\
                myuser = arg_user)
            else:
                # Look for specific dates
                # Adding ' ' as a workaround for a bug in datefinder
                match = datefinder.find_dates(' ' + command + ' ')
                try:
                    date_in = match.next()
                except:
                    response += self.grand_total(myuser=arg_user)
                else:
                    response += self.total_by_month(mydate = date_in,\
                    myuser = arg_user)
        
        # Parse for plot
        if ('plot' in command) or ('plt' in command):
            self.plot(channel)

        # Parse for the set paid tag
        if 'set paid' in command:
            response += self.set_paid_tag()
        
        # Parse for the upaid tag
        if 'set unpaid' in command:
            response += self.set_unpaid_tag()
        
        # Parse for the get paid tag
        if ('get paid' in command) or ('show paid' in command) or ('view paid' in command):
            response += self.get_paid_tag()
        
        # Parse for the get comm
        if ('show comm' in command) or ('list comm' in command) or ('view comm' in command):
            response += self.get_comm()
        
        # Parse for from paid
        if ('from paid' in command):
            arg_user = ''
            if ('me' in command) or ('my' in command):
                arg_user = user
            response += self.from_paid(myuser = arg_user)
     
        # Parse for help
        if 'help' in command:
            response += self.help()

        #else:
        #    response += "Sorry I don't understand the command: " + command + ". " + self.help()
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
            self.myshop.add_data_point(user, command, typex, date, amount)
        except ValueError:
            print "Error adding value to DF"
        else:
            return "OK! Adding {} in {}.".format(amount, typex)
    
    def grand_total(self, **kwargs):
        """ What do do when keyword "total" is found within command """
        # Total for a specific user
        if ('myuser' in kwargs) and kwargs['myuser']:
            total = self.myshop.get_grand_total(user=kwargs['myuser'])
        # Grand total
        else:
            total = self.myshop.get_grand_total()
        return '\nGrand total (*ALL DATA*):\n' + str(total).split('dtype')[0]
   

    def total_by_month(self, **kwargs):
        """ What do do when keyword "total" is found within command
            AND we have a date """
        # Total for a specific date range
        if 'mydate' in kwargs:
            min_date = str(kwargs['mydate'].year) + '{:02d}'.format(kwargs['mydate'].month) + '01'
            max_date = str(kwargs['mydate'].year) + '{:02d}'.format(kwargs['mydate'].month) + '31'
        else: 
            return "Error in total by month. Need to specify date range"
       
        # Total for a specific data range AND user
        if ('myuser' in kwargs) and kwargs['myuser']:
            total = self.myshop.get_total_by_date(min_date=min_date, max_date=max_date,\
            user=kwargs['myuser'])
        else:   
            total = self.myshop.get_total_by_date(min_date=min_date, max_date=max_date)
       
        return '\nTotal for *' + kwargs['mydate'].strftime("%B") + '*, *' + \
        str(kwargs['mydate'].year) + '*\n' + str(total).split('dtype')[0]
    
    def plot(self, channel):
        """ Plotting capability. It saves a matplotlib image file to disk and
            uploads it to Slack. 
        """
        # Image generation and local storage
        total = self.myshop.get_grand_total()
        D = total.to_dict()
        plt.bar(range(len(D)), D.values(), align='center', color='black')
        plt.xticks(range(len(D)), list(D.keys()))
        plt.ylabel('SEK', fontsize=11)
        plt.xlabel('Category', fontsize=11)
        plt.savefig('imgs/foo.png')
        
        # Uploading to Slack
        verif_token = os.getenv('MYTOKEN')
        cmd = 'curl -F file=@' + '~/imgs/foo.png -F \
        channels=' + channel + ' -H "Authorization: Bearer ' + verif_token + '" \
        https://slack.com/api/files.upload'
        (status, output) = commands.getstatusoutput(cmd)
        match = re.search(r'"ok":(\w+),', output)
        if match:
            if 'true' not in match.group(1): 
                return 'Could not plot, sorry'
        else: return 'Could not plot, sorry'
        return 'Done.'

    def set_paid_tag(self):
        self.myshop.set_tag('_P')
        return "Setting everything to *paid*."
    
    def set_unpaid_tag(self):
        self.myshop.del_tag('_P')
        return "Setting everything to *unpaid*."
    
    def get_paid_tag(self):
        result = self.myshop.get_tag('_P')
        return "Everything is paid until (and including): " + str(result)
    
    def get_comm(self):
        #result = '\n'.join(self.myshop.get_comm())
        result = self.myshop.get_comm().to_string(index=False, header=False)
        return "Entries for the *current* month:\n\n" + result
   

    def from_paid(self, **kwargs):
        """ Total from last paid """

        # Total for a specific date range
        min_date1 = datefinder.find_dates(self.myshop.get_tag('_P'))
        min_date2 = min_date1.next() 
        min_date3 = min_date2 + datetime.timedelta(days=1)
        min_date = str(min_date3.year) + '{:02d}'.format(min_date3.month) + '{:02d}'.format(min_date3.day) 
        max_date = datetime.date.today()
        max_date = str(max_date.year) + '{:02d}'.format(max_date.month) + '{:02d}'.format(max_date.day) 

        # Total for a specific user
        if ('myuser' in kwargs) and kwargs['myuser']:
            total = self.myshop.get_total_by_date(min_date=min_date, max_date=max_date,\
            user=kwargs['myuser'])
            return 'Total unpaid for ' + kwargs['myuser'] + ' from: ' + min_date + ' to ' + max_date + \
            '\n' + str(total).split('dtype')[0]
        else:   
            total = self.myshop.get_total_by_date(min_date=min_date, max_date=max_date)
            return 'Grand total unpaid from: ' + min_date + ' to ' + max_date + \
            '\n' + str(total).split('dtype')[0]



    def help(self):
        """ What do do when help keyword is found within command """
        response = "I am here to help :smile:. Currently I support commands\
        for the following categories: "
        response += ', '.join(list(self.data_cat)) + '. '
        response += 'Here are a few examples of what you can do:\n\n\
                     *Add expense*\n -Food 300.\n -I spent 150 in a bar\n -300 in home\n\n\
                     *View*\n -Total\n -Total this month \n -Total for 05/2018 \n -Total for me in July \n -plot\n\n\
                     *Payment*\n -Set paid\n -Set unpaid\n -View paid\n\n\
                     *Entries*\n -Show comm\n -List comm\n -View comm'
          
             
        return response

