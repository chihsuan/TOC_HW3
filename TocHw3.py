# !/usr/bin/evn python
# -*- coding: utf8 -*-

'''
Name: 黃啟軒
Student nubmer: F84004022

-python version: 2.7.3

-purpose:
	use 'regular_expression' to parse real-price housing information in our country, and find the average of all sale prices matching the condition as the arguments.

-argurments:
	1. url, such as http://www.datagarage.io/api/5365dee31bc6e9d9463a0057
	2  specify the town, zone name in the column
	3. specify the road name in column
	4. specify the "year" in column'''

import re
import  sys
import json
import urllib2

# use arg1 URL to get json data
def getData():
	
	# make sure that we can get data from server
	try:
		response = urllib2.urlopen( sys.argv[1] )
	except urllib2.HTTPError, e:
		print "Cannot retrieve URL: HTTP Error Code", e.code
		sys.exit(0)
	except urllib2.URLError, e:
			print "Cannot retrieve URL: " + e.reason[1]
			sys.exit(0)


	# convert to json format
	data = json.load( response, encoding = ('utf-8') )	
	
	return data

# find avg real_price that is match the argument condition
def filterData(data, township, road, year):
	
	# unicode zh-tw string to 'utf-8' for find value in data
	tw_township = unicode("鄉鎮市區", "utf-8")
	tw_road_area = unicode("土地區段位置或建物區門牌", "utf-8")
	tw_year = unicode("交易年月", "utf-8")
	tw_price = unicode("總價元", "utf-8")

	# unicode the argumament variable to 'utf-8' for match data 
	township = unicode( township, "utf-8")
	try:
		year = int( unicode( year, "utf-8" ) )
	except ValueError:
		print "Error!", year, "is not a integer"
		sys.exit(0)

	# regular expression compile pattern for reuse in following search
	pattern = re.compile( road )

	total_price = 0
	match_number = 0

	# start to match data
	for datum in data:
		# check that data's key is same to our json format
		if tw_township in datum and tw_road_area in datum \
				and tw_year in datum and tw_price  in datum:
			# match
			if datum[tw_road_area] and township == datum[tw_township] \
					and pattern.search( datum[tw_road_area].encode("utf8") ) \
						and (datum[ tw_year ] / 100)  >= year:
				total_price += int( datum[tw_price] )
				match_number += 1
		else:
			print "Error json format is not match!" 
			sys.exit(0)

	# return avg total_price
	try:
		return int( total_price / match_number )
	#if divide by zero
	except ZeroDivisionError:
		print 'No Match any result!'
		sys.exit(0)


# run program
if len( sys.argv ) == 5:
	data = getData()
	result = filterData(data, sys.argv[2], sys.argv[3], sys.argv[4])
	print result
else:
	print "ERROR len(argv) should be 4"
