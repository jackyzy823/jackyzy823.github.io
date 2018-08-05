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
    'en': ('en_US.utf8','%a, %d %b %Y'),
    'jp': ('ja_JP.utf8','%Y-%m-%d(%a)'),
    'zh': ('zh_CN.utf8','%Y年%m月%d日')
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

ARTICLE_LANG_URL = '{category}/{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = '{category}/{slug}-{lang}.html'



THEME = "./hikaru"

#Comment system customize
STATICMAN_API_ENDPOINT = "https://api.staticman.net/v2/entry/jackyzy823/jackyzy823.github.io/source/"
COMMENTS_PATH = "_data/comments"


import os
import os.path
import json


import sys
import locale
import six

def readComments(f):
    with open(f,"r") as c:
        return json.load(c)

#TODO: sorted
COMMENTS = { p : sorted([ readComments(os.path.join(COMMENTS_PATH,p,i)) 
                            for i in os.listdir(os.path.join(COMMENTS_PATH,p)) if os.path.isfile(os.path.join(COMMENTS_PATH,p,i))  
                        ],key=lambda x:x["date"])    
                        for p in os.listdir(COMMENTS_PATH) if os.path.isdir(os.path.join(COMMENTS_PATH,p)) }

def commentdate(value,articleinfo):
    from pelican.utils import strftime,SafeDatetime
    from pelican.settings import DEFAULT_CONFIG
    if hasattr(articleinfo, 'lang') and articleinfo.lang in DATE_FORMATS:
        date_format = DATE_FORMATS[articleinfo.lang]
    else:
        date_format = DEFAULT_CONFIG['DEFAULT_DATE_FORMAT']
    if isinstance(date_format, tuple):
        locale_string = date_format[0]
        if sys.version_info < (3, ) and isinstance(locale_string,
                                                    six.text_type):
            locale_string = locale_string.encode('ascii')
        locale.setlocale(locale.LC_ALL, locale_string)
        date_format = date_format[1]
    return strftime(SafeDatetime.fromtimestamp(value),date_format)
    pass

JINJA_FILTERS = { 'commentdate' : commentdate }
#TODO: support comment markdown
