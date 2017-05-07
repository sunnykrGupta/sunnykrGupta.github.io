#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sunny KUMAR'
SITENAME = u'Daemon Blog'

#Production Mode
SITEURL = 'https://sunnykrGupta.github.io'

#Devel Mode, always give absolute URL
#SITEURL = 'http://localhost:8000'

THEME = "/home/daemonsl/Dropbox/boxSpace/CodeCave/pelican-svbhack"

TIMEZONE = 'Asia/Calcutta'
DEFAULT_LANG = u'en'

PATH = 'content'

DEFAULT_METADATA = {
    'status': 'draft',
}
#Status: published
#Status: draft

#We are using share_post plugin to enable share feature in blog
# Download : https://github.com/getpelican/pelican-plugins
PLUGIN_PATHS = ['/home/daemonsl/Dropbox/boxSpace/CodeCave/pelican-plugins']
PLUGINS = ['share_post']

DELETE_OUTPUT_DIRECTORY = "True"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

#to use Google Analytics, set this var to your UA-XYZ code
GOOGLE_ANALYTICS="UA-63834161-1"

# Set this to your Disqus sitename to enable disqus comments in articles
# Set the disqus Sitename here. Goto
DISQUS_SITENAME='sunnydaemon'

STATIC_PATHS = ['images']

#replace the logo placeholder, put your logo in content/images/your_logo.png and make this var point to SITEURL + '/static/images/your_logo.png'
USER_LOGO_URL=SITEURL+'/images/logo.jpg'

# some text rendered right below the logo
TAGLINE="Data Engineer, DevOps on Kubernetes, SysAdmin, Programmer, Optimist, Footballer :D"

# set this to True if you want to enable the Internet Defense League code
INTERNET_DEFENSE_LEAGUE=True

# Social widget
SOCIAL = (
            ('github', 'https://github.com/sunnykrGupta'),
            ('twitter', 'https://twitter.com/Sunny_KrGupta'),
            ('linkedin', 'https://www.linkedin.com/in/sunnykrgupta/'),
            ('googleplus', 'https://plus.google.com/u/0/+SunnyKrGUPTA'),
            ('mail', 'mailto:sunnygupta.kr@gmail.com'),
        )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#DISPLAY_RECENT_POSTS_ON_SIDEBAR=True
