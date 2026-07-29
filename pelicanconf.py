#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

# Site URL configuration - use environment variable or default to localhost
SITEURL = os.getenv('SITEURL', 'http://localhost:8000')

# Examples:
# For development: export SITEURL='http://localhost:8000'
# For production: export SITEURL='https://sunnykrGupta.github.io'

THEME = "./pelican-svbhack-responsive"

DEFAULT_METADATA = {
    'status': 'draft',
}
#Status: unpublished
#Status: published
#Status: draft

# ------ Site settings ------ #
AUTHOR = u'Sunny Kumar'
SITENAME = u'Daemon Blog'
# some text rendered right below the logo
TAGLINE="Bits of Cloud Wisdom &Phi;  &#9679; Platform Engineer &Xi;  &#9679; Football Enthusiast &infin; &#9679; "

# Social widget
SOCIAL = (
            ('linkedin', 'https://www.linkedin.com/in/sunnykrgupta/'),
            ('github', 'https://github.com/sunnykrGupta'),
            ('x', 'https://x.com/Sunny_KrGupta'),
            ('medium', 'https://medium.com/@sunnykrgupta/'),
            ('mail', 'mailto:hello@sunnykrgupta.com'),
        )

DEFAULT_PAGINATION = 20
WITH_FUTURE_DATES = True

TIMEZONE = 'Asia/Calcutta'
DEFAULT_LANG = u'en'

PATH = 'content'

DELETE_OUTPUT_DIRECTORY = "True"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Use Google Analytics, set this var to your G-<MEASUREMENT ID>
GOOGLE_ANALYTICS =  "G-GKLD6RJQR8"
STATIC_PATHS = ['images']

#replace the logo placeholder, put your logo in content/images/your_logo.png and make this var point to SITEURL + '/static/images/your_logo.png'
USER_LOGO_URL=SITEURL+'/images/logo.jpg'

# #X (Twitter) Widget
# widget_profile_url = "https://x.com/Sunny_KrGupta"
# widget_profile_name = "@Sunny_KrGupta"

#http://docs.getpelican.com/en/stable/settings.html
#SUMMARY_MAX_LENGTH = 10  #Default 50

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#DISPLAY_RECENT_POSTS_ON_SIDEBAR=True
