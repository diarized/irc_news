#!/usr/bin/env python

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.internet.task import LoopingCall
# from twisted.python import log

import plugins
import time


class RSSFeederProtocol(irc.IRCClient):
    def __init__(self, nick):
        self.nick = nick

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
        # self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        # self.logger.log("<%s> %s" % (user, msg))
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


class IRCClientFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        proto = RSSFeederProtocol('SPurrrBot')
        proto.factory = self
        return proto

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    my_irc_client = IRCClientFactory('#999net')
    reactor.connectTCP('irc.freenode.net', 6667, my_irc_client)
    rss_sucker = RSSSucker(my_irc_client)
    lc = LoopingCall(rss_sucker.get_feed)
    lc.start(300)
    reactor.run()
