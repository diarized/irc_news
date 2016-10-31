#!/usr/bin/env python

# Based on Twisted PluginLogBot example.
# Author: Artur Kaminski
# artur@monitor.stonith.pl
# diarized@GitHub

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time
import sys
import pprint
import plugins

reload(sys)
sys.setdefaultencoding('utf8')


class Pluginer(object):
    """ Search interface to HN and other feeds """
    def __init__(self):
        self.nothing = 'nothing'

    def command(self, message):
        cmd_fields = message.split()
        # cmd_fields[0] is my nick
        cmd = cmd_fields[1]
        arguments = cmd_fields[2:]
        reload(plugins)
        try:
            plugin = getattr(plugins, cmd)
        except AttributeError:
            plugin_output = ["I do not know what '{}' means.".format(cmd)]
        else:
            plugin_output = plugin(arguments)
            # pprint.pprint(plugin_output)
        return plugin_output

    def close(self):
        pass


class PluginLogBot(irc.IRCClient):
    """A logging IRC bot."""

    nickname = "Spurr1Bot"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.pluginer = Pluginer()

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    # callbacks for events
    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.msg(channel, "[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        # self.msg(channel, "<%s> %s" % (user, msg))
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        if msg == 'help':
            self.msg(
                channel,
                'Give me an order, like "{}: ddg ircbot".'.format(
                    self.nickname
                )
            )

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            self.msg(channel, "<%s> %s" % (self.nickname, msg))
            responses = self.pluginer.command(msg)
            if not len(responses):
                return
            try:
                for response in responses:
                    self.msg(channel, response.encode("utf8"))
                    time.sleep(1) # Be polite, no flooding
            except TypeError:
                self.msg(channel, 'No responce from {}'.format(msg))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.msg(channel, "* %s %s" % (user, msg))

    # irc callbacks
    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        # old_nick = prefix.split('!')[0]
        # new_nick = params[0]
        # self.msg(channel, "%s is now known as %s" % (old_nick, new_nick))

    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'


class PluginBotFactory(protocol.ClientFactory):
    """A factory for PluginLogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename

    def buildProtocol(self, addr):
        p = PluginLogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        time.sleep(12) # Have I flooded the channel?
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)

    # create factory protocol and application
    # f = PluginBotFactory(sys.argv[1], sys.argv[2])
    f = PluginBotFactory('#998net', '/tmp/logbot.log')

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
