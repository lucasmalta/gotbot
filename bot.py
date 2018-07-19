#!/home/lucas/anaconda2/bin/python
"""
Slack Bot class

"""
import os
import time
import event
from slackclient import SlackClient

class Bot(object):
    """ Class that implements and initializes bot API connection """
    def __init__(self):
        """ Authentication with OAuth """
        # Get verification token stored as an enviromental variable
        self.verif_token = os.environ.get("MYTOKEN")
        self.slack_client = SlackClient(self.verif_token)
        self.bot_name = "gotbot"
        self.bot_id = self.get_bot_id()
        if self.bot_id is None:
            exit("Error, could not find " + self.bot_name)
        self.event = event.Event(self)
        self.listen()

    def get_bot_id(self):
        """ Check if bot ID in Slack """
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return "<@" + user.get('id') + ">"
            return None

    def listen(self):
        """ Listen to Slack real-time events """
        if self.slack_client.rtm_connect(with_team_state=False):
            print "Successfully connected, listening for commands"
            while True:
                self.event.wait_for_event()
                time.sleep(1)
        else:
            exit("Error, Connection Failed")

