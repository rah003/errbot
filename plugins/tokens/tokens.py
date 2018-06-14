import gspread
import json
import os

from errbot import BotPlugin, botcmd
from oauth2client.service_account import ServiceAccountCredentials


class Tokens(BotPlugin):
    """
    This is a very basic plugin to try out listing of current ownership of tokens and queue for integration.
    """

    version_map = {}

    def get_token_column(self, wks, which_token):
        if (which_token in self.version_map):
            return self.version_map[which_token]

        token_col = 0
        # listing 63 columns triggers OOME on heroku free dyno
        for x in list(range(1, 10)):
            if wks.cell(1, x).value == which_token:
                token_col = x
                break

        self.version_map[which_token] = token_col

        return token_col

    def token_status(self, wks, which_token, token_type):
        """
        Find tokens
        :param wks: current workspace
        :param which_token: to specific list version (5.4, 5.5, 5.6 ...)
        :param token_type: to list queue (q) vs. current ownership of token (p)
        :param token_col: column holding info about specific list version (5.4, 5.5, 5.6 ...)
        :return: string with info about given version and token request type
        """

        # find column holding values for branch of interest
        token_col = self.get_token_column(wks, which_token)

        # iterate through the values until we find someone who's processing => holding token right now
        token_column_values = wks.col_values(token_col)

        # total count
        # print('len:' + str(len(values_list)))

        row_count = 0
        results = []
        for token_value in token_column_values:
            row_count = row_count + 1
            if token_value == token_type:
                person = wks.cell(row_count, 2).value
                reason = wks.cell(row_count, 3).value
                # TODO: convert list of ppl results into list of person-reason tuples.
                if not (person in results):
                    results.append(person)

        be = 'is'
        hold = 'holds'
        if len(results) > 1:
            be = 'are'
            hold = 'hold'

        if len(results) == 0:
            persons = 'no one'
        else:
            persons = str(results).strip('[]')

        if token_type == 'p':
            result = '**'+persons+'** '+hold+' token'
            # print("res:"+result)
        else:
            if len(results) == 0:
                persons = 'and no one'
            # print("number of results:" + str(len(results)))
            result = '**' + persons + '** ' + be + ' queued for one'
            # print(result)

        return result

    @botcmd  # flags a command
    def listtokens(self, msg, args):  # a command callable with !listtokens
        """
        Execute to check who holds the token and how long is the queue.
        """

        # read from system properties
        url_prop = os.getenv('token_sheet_url')
        creds_json_prop = os.getenv('token_sheet_creds')

        scope = ['https://spreadsheets.google.com/feeds']
        dictionary = json.loads(creds_json_prop, strict=False)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(dictionary, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_url(url_prop)
        wks = sheet.worksheet('TOKEN_Q')

        if not args:
            # empty list of args, get all
            args = '5.6 5.5 5.4'

        res = 'I think that '
        count = 0
        for x in args.split():
            res = res + self.token_status(wks, x, 'p')+' and '+self.token_status(wks, x, 'q')
        return res  # This string format is markdown.

