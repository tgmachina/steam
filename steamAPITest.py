#!/usr/bin/python2.7

'''
	Playing with the Steam API (application programming interface)

	Useful links:
		Steam web API docs: http://steamcommunity.com/dev
		Player data API (what I'll be using): https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0001.29

	This file will be a simple demonstration of how to get data from steam using python.
	
	Steps to using this:
		1. Get an API key (instructions below) and paste replace the whole <REPLACE_WITH_YOUR_KEY> section.
		2. Run the script python steamAPITest.py
'''

# This library is used to make HTTP requests.
# This is similar to what your browser does when you type
# https://www.google.com
import urllib2
# JSON = JavaScript object notation. Don't worry about what
# that means, only that its a data exchange format. Its akin
# to a set number of packages that UPS offers. When you know
# how big and what shape a package is, they get very easy to stack
# and ship.
import json

'''
	To get an API key, go to the first useful link I posted,
	http://steamcommunity.com/dev, and follow the instructions
	for "Obtaining an Steam Web API Key". When it asks for your
	domain, just put in "localhost".
'''
API_KEY = '<REPLACE_WITH_YOUR_KEY>'
API_URL_ROOT = 'http://api.steampowered.com'

"""
	I built 2 utility functions, build_url_generator and
	build_query to help with creating a URL to talk to steam.
	The urls are in the format:
	http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>

	build_url_generator returns another function that takes a query
	string as a parameter (which build_query does).

	I'll give examples of using these below
"""

"""
	build_url_generator:
		interface: where the data comes from (e.g. ISteamUser)
		method: the way you get that data (e.g. GetPlayerSummaries)
		version: version of the API, listed with the method (e.g. v0002)
"""
def build_url_generator(interface, method, version):
	request_uri = "/".join([API_URL_ROOT, interface, method, version])
	return (lambda query_string : request_uri + query_string)

"""
	build_query:
		options: the arguments to the function, ranging from appid,
		gameid, format, steamids, etc
	
	The options (arguments) change for every method, so you'll have
	to refer to the API documentation about the particular
	method you want to use
"""
def build_query(options):
	query_string = "?key=" + API_KEY + "&"
	for key in options:
		query_string = query_string + key + "=" + options[key] + "&"
	return query_string

def test_get_friends_list():
	sample_options = {
			 # Your steam ID exadiz = 76561197972294203
			'steamid' : '76561197972294203',
			'relationship' : 'friend'
	}

	# Make the URL generator
	url_gen = build_url_generator('ISteamUser', 'GetFriendList', 'v0001')

	# Build the URL with the query string
	request_url = url_gen(build_query(sample_options))

	# You can try the url in the browser even uncomment this:
	# print request_url
	# and copy and paste it from the terminal into the browser

	response = urllib2.urlopen(request_url)

	# JSON is returned as a string so I have to turn it into a
	# python dictionary
	decoded_json = json.loads(response.read())

	friends = decoded_json['friendslist']['friends']

	return friends

friends = test_get_friends_list()

# There are other attributes returned, but this is just an
# example of what you can do.
for friend in friends:
	print friend['friend_since']
