#!/home/lucas/anaconda2/bin/pytho
"""
Slack Event class

"""

import command

class Event:
    """ Handle Slack real-time events """
    def __init__(self, bot):
        """ Constructor """
        self.bot = bot
        self.command = command.Command()
     
    def wait_for_event(self):
        """ Wait for real-time events """
        events = self.bot.slack_client.rtm_read()
         
        if events and len(events) > 0:
            for event in events:
                #print event
                self.parse_event(event)
                 
    def parse_event(self, event):
        """ Look for our bot-related events"""
        if event and 'text' in event and self.bot.bot_id in event['text']:
            self.handle_event(event['user'], event['text'].\
            split(self.bot.bot_id)[1].strip().lower(), event['channel'])
 
    def handle_event(self, user, xcommand, channel):
        """ Get response and send it to Slack """
        if xcommand and channel:
            print "Received command: " + xcommand + " in channel: " + channel +\
            " from user: " + user
            response = self.command.handle_command(user, xcommand, channel)
            self.bot.slack_client.api_call("chat.postMessage", channel=channel,\
            text=response, as_user=True)
