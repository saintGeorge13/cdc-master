# -*- coding: UTF-8 -*- 
# activate_this = '/var/www/hitme/hitme/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))


import sys
import site

site.addsitedir('/var/www/hitme/hitme/lib/python3.7/site-packages')
site.addsitedir('/usr/local/Python-3.7.7/Lib')
sys.path.insert(0, '/var/www/hitme')
# sys.path.insert(1, '/var/www/hitme/lib')
from server import app as application


if __name__ == "__main__":
    application.run()