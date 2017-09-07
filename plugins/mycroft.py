from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import re

class Mycroft(BotPlugin):
    """
    ask questions about mycroft and interact with a mycroft instance
    """

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @re_botcmd(pattern=r"doc.*mycroft|mycroft.*doc.*", prefixed=False, flags=re.IGNORECASE)
    def mycroft_docs(self, message, match):
        """A command which gives you the location to the mycroft documentation"""
        return "The mycroft documentation can be found at https://docs.mycroft.ai"

    @re_botcmd(pattern=r"install.*mycroft|mycroft.*install.*", prefixed=False, flags=re.IGNORECASE)
    def install_mycroft(self, message, match):
        """A command which gives you the location to the mycroft documentation"""
        return "The information for installing mycroft can be found here, https://docs.mycroft.ai/installing.and.running"
