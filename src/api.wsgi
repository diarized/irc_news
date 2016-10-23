import sys
sys.path.insert(0, '/home/artur/Scripts/Python/src/irc_news/src')

activate_this = '/home/artur/Scripts/Python/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from api import app as application
