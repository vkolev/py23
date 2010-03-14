#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       py23.py
#
#       Copyright 2009 Vladimir Kolev <vladi@vladimirkolev.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import urllib, urllib2
from xml.dom import minidom as dom

__author__ = "Vladimir Kolev <vladi@vladimirkolev.com>"
__version__ = "0.1"
__license__ = "GNU/GPLv3"

""" py23 is a simple api wrapper for edno23.com isnpired from ruby23 written by Mitko Kostov"""

""" Constant API_INFO - the link to the information api
    and API_POST - link to the posting api"""
API_INFO = "http://edno23.com/api/xml/get.php"
API_POST = "http://edno23.com/api/xml/post.php"


def followers(user):
    """
    Get information about the users following the user giving as parameter the username

    @type user: string
    @param user: the username, being are checked
    @rtype: structured XML data string
    @return: who is following our user
    """

    type = 'followers'
    # Encode the username and the type to fit in the url
    eUsername = urllib.urlencode(dict(username=user))
    eType = urllib.urlencode(dict(type=type))
    # Generate the encoded URL
    url = '%s?%s&%s' % (API_INFO, eUsername, eType)
    try:
        # Send a requested url and read the result
        request = urllib.urlopen(url)
        responde = request.read()
        # Checks id the username is existing
        if ("<status>OK</status>" in responde):
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e

def following(user):
    """
    Get information about who the user is following giving as parameter the username

    @type user: string with the username
    @param user: username
    @rtype: structured XML data string
    @return: who our user is following
    """
    type = 'following'
    # Encode the username and the type to fit in the url
    eUsername = urllib.urlencode(dict(username=user))
    eType = urllib.urlencode(dict(type=type))
    # Generate the encoded url
    url = '%s?%s&%s' % (API_INFO, eUsername, eType)
    try:
        # Send the requested url and read the result
        request = urllib.urlopen(url)
        responde = request.read()
        # Cheks if the username is existing
        if ("<status>OK</status>" in responde):
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e

def userinfo(user):
    """
    Get information about who the user

    @type user: string with the username
    @param user: username
    @rtype: structured XML data string
    @return: who our user is"""
    type = 'userinfo'
    eUsername = urllib.urlencode(dict(username=user))
    eType = urllib.urlencode(dict(type=type))
    url = '%s?%s&%s' % (API_INFO, eUsername, eType)
    try:
        info = {}
        request = urllib.urlopen(url)
        responde = request.read()
        if ("<status>OK</status>" in responde):
            # Return the userinformation
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e

def following_posts(user):
    """
    Get the posts from the users who our user is following giving as parameter the username
    @type user: string
    @param user: the username, being checked
    @rtype: structured XML data
    @return: posts of the followed by our user"""
    type = 'following_posts'
    # Encode the username and the type to fit in the URL
    eUsername = urllib.urlencode(dict(username=user))
    eType = urllib.urlencode(dict(type=type))
    # Generate the encoded URL
    url = '%s?%s&%s' % (API_INFO, eUsername, eType)
    try:
        # Send the request and read the result
        request = urllib.urlopen(url)
        responde = request.read()
        # Check if the username is valid
        if ("<status>OK</status>" in responde):
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e

def posts_mention_me(user):
    """
    Get the posts where our user is mentioned

    @type user: string
    @param user: the username being checked
    @rtype: structured XML data string
    @return: the posts where our user is mentioned
    """
    type = 'posts_mention_me'
    eUsername = urllib.urlencode(dict(username=user))
    eType = urllib.urlencode(dict(type=type))
    url = '%s?%s&%s' % (API_INFO, eUsername, eType)
    try:
        request = urllib.urlopen(url)
        responde = request.read()
        if ("<status>OK</status>" in responde):
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e

def direct_posts_from_me(user, password):
    """
    Get the posts created by our user - this method uses a basic authentication with username and password

    @type user: string
    @param user: the username being checked
    @type password: string
    @param password: the B{password} of that B{user}
    @rtype: structured XML data string
    @return: the posts created by the B{user}
    """
    type = 'direct_posts_from_me'
    eUsername = urllib.urlencode(dict(username=user))
    eType = urllib.urlencode(dict(type=type))
    url = '%s?%s&%s' % (API_INFO, eUsername, eType)
    try:
        # Creating a password manager to send the password
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # Add the username, the password and the associated URL
        passman.add_password(None, url, user, password)
        # Create our authentication handler
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        # Use the authentication hadler for opening the URL
        opener = urllib2.build_opener(authhandler)
        # Install our opener and authenticate
        urllib2.install_opener(opener)
        # Open the url and read the result
        request = urllib2.urlopen(url)
        responde = request.read()
        # This part is not needed actually, since we will get an error
        # if the password and the username doesn't match
        if ("<status>OK</status>" in responde):
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e
""" Get the posts send to our user, this time we give as parameter the username and the password
    becouse edno23 requires a basic HTTP authenticatio.

    returns a structured XML dat"""
def direct_posts_to_me(user, password):
    """
    Get the posts created by our user

    @type user: string
    @param user: the username being checked
    @type password: string
    @param password: the B{password} of the B{user}
    @rtype: structured XML data string
    @return: posts created by the B{user}
    """
    type = 'direct_posts_to_me'
    eUsername = urllib.urlencode(dict(username=user))
    eType = urllib.urlencode(dict(type=type))
    url = '%s?%s&%s' % (API_INFO, eUsername, eType)
    try:
        # Creating a password manager to send the password
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # Add the username, the password and the associated URL
        passman.add_password(None, url, user, password)
        # Create our authentication handler
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        # Use the authentication hadler for opening the URL
        opener = urllib2.build_opener(authhandler)
        # Install our opener and authenticate
        urllib2.install_opener(opener)
        # Open the url and read the result
        request = urllib2.urlopen(url)
        responde = request.read()
        # This part is not needed actually, since we will get an error
        # if the password and the username doesn't match)
        if ("<status>OK</status>" in responde):
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e

""" This method is for posting to edno23 requires more information and also needs
    the username and the password for the user, who is posting."""
def post(apiid, apipass, message, attachedlink, user, password):
    """
    Create a post in edno23 with link

    @type apiid: URL
    @param apiid: the API for posting I{http://edno23.com/api/xml/post.php}
    @type apipass: string
    @param apipass: the password for the psot API
    @type message: string
    @param message: The message beeing posted
    @type attachedlink: URL
    @param attachedlink: Attached link to the post
    @type user: string
    @param user: The B{user} creating the post
    @type password: string
    @param password: The B{password} of the B{user}
    @rtype: structured XML data string
    @return: respond of the server OK - NOT OK :)
    """
    eApiId = urllib.urlencode(dict(api_id=apiid))
    eApiPass = urllib.urlencode(dict(api_pass=apipass))
    eAttachedLink = urllib.urlencode(dict(attached_link=attachedlink))
    eUsername = urllib.urlencode(dict(username=user))
    url = '%s?%s&%s&%s&%s&%s' % (API_POST, eApiId, eApiPass, eAttachedLink, eUsername, password)
    try:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, user, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        request = urllib2.urlopen(url)
        responde = request.read()
        if ("<status>OK</status>" in responde):
            return responde
        else:
            return "ERROR: Invalid username %s" % user
    except IOError, e:
        return "ERROR: %s" % e

def char_data(data):
    return repr(data)
#def start_follow(username, follower):
#    print
