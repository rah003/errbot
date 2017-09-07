from errbot import BotPlugin, botcmd, arg_botcmd, webhook


class Mycroft(BotPlugin):
    """
    ask questions about mycroft and interact with a mycroft instance
    """

    @webhook
    def example_webhook(self, incoming_request):
        """A webhook which simply returns 'Example'"""
        return "Example"

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def mycroft_docs(self, message, args):
        """A command which gives you the location to the mycroft documentation"""
        return "The mycroft documentation can be found at https://docs.mycroft.ai"