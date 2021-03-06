#!/usr/bin/env python
#coding:utf-8
from lib.core.data import paths
import sys
import os
from lib.core.settings import INVALID_UNICODE_CHAR_FORMAT
from lib.core.settings import banner as banner1
from lib.core.log import logger
from thirdparty import hackhttp
import urlparse
import urllib2,urllib
"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """

    return hasattr(sys, "frozen")

def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))

def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return "NULL"

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or "utf8")
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, "utf8")
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    elif isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances

def setPaths(rootPath):
    """
    Sets absolute paths for project directories and files
    """

    paths.w9scan_ROOT_PATH = rootPath

    # sqlmap paths
    paths.w9scan_Plugin_Path = os.path.join(paths.w9scan_ROOT_PATH, "plugins")

def banner():
    print banner1

def makeurl(url):
    prox = "http://"
    if (url.startswith("https://")):
        prox = "https://"
    url_info = urlparse.urlparse(url)
    url = prox + url_info.netloc + "/"
    return url

def Get_lineNumber_fileName():
    File_Obj = sys._getframe().f_back

    f_line = File_Obj.f_lineno  # get code line
    f_co_name = File_Obj.f_code.co_name  # get code function

    try:
        ff_line = File_Obj.f_back.f_lineno
        ff_co_name = File_Obj.f_back.f_code.co_name

    except:
        ff_co_name = File_Obj.f_code.co_filename
        ff_line = f_line

    logger.info('%s:%d <= %s:%d' % (f_co_name,
                                     f_line,
                                     ff_co_name,
                                     ff_line))

    return '%s:%d <= %s:%d' % (f_co_name,
                               f_line,
                               ff_co_name,
                               ff_line)

def createIssueForBlog(errMSG):
    """
    Automatically create a blog comment with unhandled exception information
    """
    hh = hackhttp.hackhttp()
    postData = "gid=213&pid=0&qqnum=&comname=w9scan+BugReporter&commail=buger%40hacking8.com&comurl=&private=on&comment=%5B%E7%A7%81%E5%AF%86%E8%AF%84%E8%AE%BA%5D%E6%8A%A5%E5%91%8Abug:" + errMSG
    code, head, body, redirect, log = hh.http('https://blog.hacking8.com/index.php?action=addcom', post=postData)