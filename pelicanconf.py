#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'jackyzy823'
SITENAME = u"君に会いたい ...Sprinter"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()
        
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'jp': '%Y-%m-%d(%a)',
    'zh': '%Y年%m月%d日'
}       
      

# Social widget
SOCIAL = (('me@github', 'https://github.com/jackyzy823'),
          ('me@twitter[NSFW]','https://twitter.com/jackyzy823'),
         ) 

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['extra/favicon.png',"images"]
EXTRA_PATH_METADATA = {
        'extra/favicon.png': {'path': 'favicon.png'}
}
#USE_FOLDER_AS_CATEGORY = True

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
ARTICLE_SAVE_AS = "{category}/{slug}.html"
ARTICLE_URL = "{category}/{slug}.html"
THEME = "./mytheme"
