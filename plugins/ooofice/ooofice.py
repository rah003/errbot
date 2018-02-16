import gspread
import json
import os
from datetime import date

from errbot import BotPlugin, botcmd
from oauth2client.service_account import ServiceAccountCredentials


class OOOfice(BotPlugin):
    """
    This is a very basic plugin to tell ppl I'm on hols when they mention my name.
    """

    def callback_message(self, mess):
        endday = date(2018, 2, 25)
        today = date.today()
        if mess.body.find('@yan') != -1 and today < endday:
            self.send(
                mess.frm,
                "Please be informed that Yan is on holidays until Feb 25th",
            )
        if mess.body.find('yantest') != -1 and today < endday:
            self.send(
                mess.frm,
                "gotcha",
            )


    @botcmd  # flags a command
    def whosout(self, msg, args):  # a command callable with !whosout
        """
        Test
        """
        return "you"
