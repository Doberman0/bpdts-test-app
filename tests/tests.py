import unittest
import requests

# To test the helper functions
from helper_functions import getUsers
from helper_functions import haversine

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
		keys_as_list = sorted(list(response[0].keys())) # Get a sorted list of all the keys
		self.assertEqual(keys_as_list, ['email', 'first_name', 'id', 'ip_address', 'last_name', 'latitude', 'longitude'])
		# If I had more time, I would test each type of the field as well. E.g. id is an int, email is a string
		# I would also check to make sure the formats were correct using regex

	# Testing Haversince Function
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



if __name__ == '__main__':
	unittest.main()