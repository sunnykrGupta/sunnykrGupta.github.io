#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sunny Kumar'
SITENAME = u'Daemon Blog'

#Production Mode
# SITEURL = 'https://sunnykrGupta.github.io'

#Devel Mode, always give absolute URL
SITEURL = 'http://localhost:8000'

THEME = "./pelican-svbhack-responsive"
#THEME = "/home/daemonsl/Yandex.Disk/Ydx-Space/CodeCave/pelican-svbhack-responsive"


TIMEZONE = 'Asia/Calcutta'
DEFAULT_LANG = u'en'

PATH = 'content'

DEFAULT_METADATA = {
    'status': 'draft',
}
#Status: unpublished
#Status: published
#Status: draft

#We are using share_post plugin to enable share feature in blog
# Download : https://github.com/getpelican/pelican-plugins
#PLUGIN_PATHS = ['/home/daemonsl/Yandex.Disk/Ydx-Space/CodeCave/pelican-plugins']
#PLUGINS = ['share_post']

DELETE_OUTPUT_DIRECTORY = "True"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

#to use Google Analytics, set this var to your UA-XYZ code
GOOGLE_ANALYTICS = "UA-63834161-1"

# # Set this to your Disqus sitename to enable disqus comments in articles
# # Set the disqus Sitename here. Goto
# DISQUS_SITENAME='sunnydaemon'

STATIC_PATHS = ['images']

#replace the logo placeholder, put your logo in content/images/your_logo.png and make this var point to SITEURL + '/static/images/your_logo.png'
USER_LOGO_URL=SITEURL+'/images/logo.jpg'

# some text rendered right below the logo
TAGLINE="Little wisdom of coding &Phi;  &#9679; Platform Engineer &Xi;  &#9679;  Football Lover &infin; &#9679; "

# set this to True if you want to enable the Internet Defense League code
INTERNET_DEFENSE_LEAGUE=False

# #Twitter Widget
# widget_profile_url = "https://twitter.com/Sunny_KrGupta"
# widget_profile_name = "@Sunny_KrGupta"
# widget_id_int = "605800181926199296"

# Social widget
SOCIAL = (
            ('linkedin', 'https://www.linkedin.com/in/sunnykrgupta/'),
            ('github', 'https://github.com/sunnykrGupta'),
            ('twitter', 'https://twitter.com/Sunny_KrGupta'),
            ('medium', 'https://medium.com/@sunnykrgupta/'),
            ('mail', 'mailto:sunnygupta.kr@yandex.com'),
        )

DEFAULT_PAGINATION = 10

#http://docs.getpelican.com/en/stable/settings.html
#SUMMARY_MAX_LENGTH = 10  #Default 50

WITH_FUTURE_DATES = True

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#DISPLAY_RECENT_POSTS_ON_SIDEBAR=True
