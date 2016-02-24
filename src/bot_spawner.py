#!/usr/bin/env python

from twisted.internet import reactor
import bots
import pprint

for bot_name in vars(bots):
    bot = getattr(bots, bot_name)
    pprint.pprint(bot)
    # b = bot()
    # reactor.connectTCP("irc.freenode.net", 6667, b)
    # reactor.run()
