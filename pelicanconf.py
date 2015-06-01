#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sunny KUMAR'
SITENAME = u'Daemon Blog'
SITEURL = 'http://localhost:8000'
THEME = "/home/lautner/CodeCave/pelican-svbhack"

TIMEZONE = 'Asia/Calcutta'

DEFAULT_LANG = u'en'

PATH = 'content'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

#to use Google Analytics, set this var to your UA-XYZ code
#GOOGLE_ANALYTICS=

STATIC_PATHS = ['images']

#replace the logo placeholder, put your logo in content/images/your_logo.png and make this var point to SITEURL + '/static/images/your_logo.png'
USER_LOGO_URL=SITEURL+'/images/logo.jpg'

# set this to your Disqus sitename to enable disqus comments in articles
#DISQUS_SITENAME=

# some text rendered right below the logo
TAGLINE="Data Science Enthusiast, Programmer, Optimist, Footballer :D"

# set this to True if you want to enable the Internet Defense League code
INTERNET_DEFENSE_LEAGUE=True

# Social widget
SOCIAL = (
            ('github', 'https://github.com/sunnykrGupta'),
            ('twitter', 'https://twitter.com/sunnyLaGupta'),
            ('linkedin', 'https://linkedin.com/in/sunnyO4'),
            ('mail', 'mailto:sunnylautner4@gmail.com'),
        )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR=True
