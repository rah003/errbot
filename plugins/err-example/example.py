from errbot import BotPlugin, botcmd


class Example(BotPlugin):
    """
    This is a very basic plugin to try out your new installation and get you started.
    Feel free to tweak me to experiment with Errbot.
    You can find me in your init directory in the subdirectory plugins.
    """

    def trymetoo(self, msg, args):  # a command callable with !tryme
        """
        test chaining commands
        """
        return 'It *works* !'  # This string format is markdown.

    @botcmd  # flags a command
    def tryme(self, msg, args):  # a command callable with !tryme
        """
        Execute to check if Errbot responds to command.
        Feel free to tweak me to experiment with Errbot.
        You can find me in your init directory in the subdirectory plugins.
        """
        return trymetoo(self, msg, args)  # This string format is markdown.

