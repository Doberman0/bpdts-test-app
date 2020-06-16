import unittest
import requests
import json
import re

# To test the helper functions
from helper_functions import getUsers
from helper_functions import haversine

# To test the app itself
from app import app
#from app import getAllUsersUnderFiftyMiles

class Tests(unittest.TestCase):

	# Testing the helper functions first

	def test_get_users(self):
		# Making sure that getUsers is ok
		response = getUsers()
		
		# Confirm that the request-response cycle complete successfully
		# With 1000 responses
		self.assertEqual(len(response), 1000)

		# JSON is a list of dictionaries so we need to make sure that we get JSON responses
		# type is of list
		self.assertEqual(type(response), list)
		# Make sure that the elements are dictionaries
		for test in response:
			self.assertEqual(type(test), dict)
			# Finally, we check that keys are the correct ones and only those are there
			keys_as_list = sorted(list(test.keys())) # Get a sorted list of all the keys
			self.assertEqual(keys_as_list, ['email', 'first_name', 'id', 'ip_address', 'last_name', 'latitude', 'longitude'])
			# Test each type of the field as well. E.g. id is an int, email is a string
			self.assertEqual(type(test['id']), int)
			self.assertEqual(type(test['first_name']), str)
			self.assertEqual(type(test['last_name']), str)
			self.assertEqual(type(test['email']), str)
			self.assertEqual(type(test['ip_address']), str)


	# Testing Haversince Function
	# Note: This is all backend and will never receive non-numerical values,
	# 		so there's no need to test for it
	def test_get_users_positives(self):
		hav = round(haversine(10., 20., 30., 40.), -1) # To 3sf
		# This was checked using an online calculator
		self.assertEqual(hav, 1890.) 

	def test_get_users_positives(self):
		hav = round(haversine(-10., -20., -30., -40.), -1) # To 3sf
		# This was checked using an online calculator
		self.assertEqual(hav, 1890.) 

	def test_get_users_general(self):
		hav = round(haversine(30., -20., -30., 20.), -1)
		# This was checked using an online calculator
		self.assertEqual(hav, 4910.) 

	def test_get_usersZero_distance(self):
		hav = round(haversine(30., 30., 30., 30.), -1)
		# Should be 0
		self.assertEqual(hav, 0.)

	def test_get_users_zero_values(self):
		hav = round(haversine(0., 0., 0., 0.), -1)
		# Should be 0
		self.assertEqual(hav, 0.)

	# Testing the API itself
	def test_get_all_users_in_london_within_fifty_miles(self):
		self.app = app 

		response = requests.get('http://localhost:5000/users/London')

		# What we expect to receive manual testing
		expected_response = [{"email":"agarnsworthy7d@seattletimes.com","first_name":"Ancell","id":266,"ip_address":"67.4.69.137","last_name":"Garnsworthy","latitude":51.6553959,"longitude":0.0572553},{"email":"hlynd8x@merriam-webster.com","first_name":"Hugo","id":322,"ip_address":"109.0.153.166","last_name":"Lynd","latitude":51.6710832,"longitude":0.8078532},{"email":"phebbsfd@umn.edu","first_name":"Phyllys","id":554,"ip_address":"100.89.186.13","last_name":"Hebbs","latitude":51.5489435,"longitude":0.3860497}]

		# Check that you get the correct responses
		self.assertEqual(json.loads(response.content), expected_response)

	def test_get_all_users_within_fifty_miles_random_location(self):
		# Using two random coordinates (1.0,11.0) for latitude, longitude respectively
		self.app = app 

		response = requests.get('http://localhost:5000/users/London?latitude=1.0&longitude=11.0')

		# What we expect to receive manual testing
		expected_response = [{"email":"dmaps1w@home.pl","first_name":"Dieter","id":69,"ip_address":"174.205.88.204","last_name":"Maps","latitude":1.1287179,"longitude":11.267967}]

		# Check that you get the correct responses
		self.assertEqual(json.loads(response.content), expected_response)

	def test_get_all_users_within_fifty_miles_invalid_input(self):
		# Entering invalid input such as 'foo' in place of 12.4 (for example)
		self.app = app 

		response = requests.get('http://localhost:5000/users/London?latitude=foo&longitude=11.0')

		# What we expect to receive manual testing
		expected_response = {"Error":"Please enter numerical values"}

		# Check that you get the correct responses
		self.assertEqual(json.loads(response.content), expected_response)


if __name__ == '__main__':
	unittest.main()