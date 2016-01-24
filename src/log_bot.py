#!/usr/bin/env python

# Based on Twisted LogBot example.
# Author: Artur Kaminski
# artur@monitor.stonith.pl
# diarized@GitHub

"""
An example IRC log bot - logs a channel's events to a file.

If someone says the bot's name in the channel followed by a ':',
e.g.

    <foo> logbot: hello!

the bot will reply:

    <logbot> foo: I am a log bot

Run this script with two arguments, the channel name the bot should
connect to, and file to log to, e.g.:

    $ python ircLogBot.py test test.log

will log channel #test to the file 'test.log'.

To run the script:

    $ python ircLogBot.py <channel> <file>
"""


# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys
import plugins

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file_handler):
        self.file_handler = file_handler

    def log(self, message):
        """Write a message to the file_handler."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file_handler.write('%s %s\n' % (timestamp, message))
        self.file_handler.flush()

    def close(self):
        self.file_handler.close()


class Pluginer(object):
    """ Search interface to HN and other feeds """
    def __init__(self):
        self.nothing = 'nothing'

    def command(self, message):
        # msg = "%s: I am a log bot" % user
        cmd_fields = message.split()
        cmd = cmd_fields[1]
        arguments = cmd_fields[2:]
        plugin_output = ["Looking for plugin {}".format(cmd)]
        try:
            plugin = getattr(plugins, cmd)
        except AttributeError:
            plugin_output.append("I do not know what '{}' means.".format(cmd))
        else:
            plugin_output.extend(plugin(arguments))
        # for output in plugin_output:
        #     yield output
        return plugin_output

    def close(self):
        pass


class LogBot(irc.IRCClient):
    """A logging IRC bot."""
    
    nickname = "Spurr1Bot"
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.pluginer = Pluginer()

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            self.logger.log("<%s> %s" % (self.nickname, msg))
            plugin_responses = self.pluginer.command(msg)
            for response in plugin_responses[:min([3, len(plugin_responses)])]:
                self.msg(channel, response)
                time.sleep(1)

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'



class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename

    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    # create factory protocol and application
    # f = LogBotFactory(sys.argv[1], sys.argv[2])
    f = LogBotFactory('#998net', '/tmp/logbot.log')

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
