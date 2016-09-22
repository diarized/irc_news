import ConfigParser as configparser

def get_feeds():
    config = configparser.RawConfigParser()
    config.read('rsss.cfg')
    return config.items('RSSs')
