from errbot import BotPlugin, cmdfilter
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

import dialogflow

from datetime import datetime as dt

class ApiAiPlugin(BotPlugin):
    def __init__(self, *args, **kwargs):
        super(ApiAiPlugin, self).__init__(*args, **kwargs)
        #self.apikey = os.getenv('api_io_apikey')
        #self.apiai = apiai.ApiAI(self.apikey)
        self.project_id = os.getenv('api_io_projectid')

        # read from system properties
        creds_json_prop = os.getenv('api_io_creds')

        scope = [os.getenv('api_io_token_url')]


        dictionary = json.loads(creds_json_prop, strict=False)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(dictionary, scope)

        self.session_client = dialogflow.SessionsClient(credentials=credentials)
        self.language_code = "en-US"


    @cmdfilter(catch_unprocessed=True)
    def apiai_filter(self, msg, cmd, args, dry_run, emptycmd=False):
        """DialogFlow API Detect Intent Python sample with text inputs."""
        if not emptycmd:
            return msg, cmd, args

        matched_prefix = False
        prefixes = self.bot_config.BOT_ALT_PREFIXES + (self._bot.bot_config.BOT_PREFIX,)

        for prefix in prefixes:
            if msg.body.startswith(prefix):
                matched_prefix = True

        if not matched_prefix:
            return msg, cmd, args

        # identity of person we are talking to in order to have multiple simultaneous conversations
        session_id = msg.frm.person[:36]

        session = self.session_client.session_path(self.project_id, session_id)
        print('Session path: {}\n'.format(session))

        clean_text = msg.body
        for prefix in prefixes:
            if clean_text.startswith(prefix):
                clean_text = clean_text.replace(prefix, '', 1).strip()
                break

        separators = self._bot.bot_config.BOT_ALT_PREFIX_SEPARATORS
        for sep in separators:
            if clean_text.startswith(sep):
                clean_text = clean_text.replace(sep, '', 1)

        self.log.debug("API.ai will be sent: {}".format(clean_text))

        text_input = dialogflow.types.TextInput(
            text=clean_text, language_code=self.language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = self.session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        decoded_response = response.query_result.fulfillment_text
        print('Fulfillment text: {}\n'.format(
            decoded_response))

        self.log.debug("API.ai returned: {}".format(decoded_response))

        if decoded_response['status']['errorType'] == 'success':
            speech = decoded_response['result']['fulfillment']['speech']
            if len(speech):
                return speech
            elif decoded_response['result']['action'] == 'notifications.add':
                params = decoded_response['result']['parameters']
                summary = params['summary'] if 'summary' in params else None
                parseddate = params['date'] if 'date' in params else None
                parsedtime = params['time'] if 'time' in params else None

                if not parseddate and not parsedtime:
                    return "I can't set a reminder for that time."

                if parseddate:
                    targetdate = dt.strptime(parseddate, '%Y-%d-%m').date()
                else:
                    targetdate = dt.utcnow().date()

                if parsedtime:
                    targettime = dt.strptime(parsedtime, '%H:%M:%S').time()
                else:
                    targettime = dt.utcnow().time()

                when = dt.combine(targetdate, targettime)
                secondsuntil = (when - dt.utcnow()).seconds

                self.start_poller(secondsuntil,
                                  self.notification_callback,
                                  args=(summary, secondsuntil, msg))

                return "Setting reminder for: {}".format(when)

        return

    def notification_callback(self, summary, secondsuntil, msg):
        self.stop_poller(self.notification_callback,
                         args=(summary, secondsuntil, msg))

        self.log.debug('Notification: {}'.format(summary))
        self.send(msg.frm,
                  groupchat_nick_reply=True,
                  text='Notification: {}'.format(summary))

