#!flask/bin/python
from flask import Flask
from flask import jsonify
import requests # To get users from API provided
import json
from math import radians, cos, sin, asin, sqrt
from typing import List


app = Flask(__name__)

# Helper functions
def getUsers() -> List[dict]:
	'''
	This function returns all the users from the API given
	Format is [{person1}, {person2}, ...]
	'''
	url = 'https://bpdts-test-app.herokuapp.com/users'
	response_get_request = requests.get(url)
	return json.loads(response_get_request.content)

def haversine(lat1:float, lon1:float, lat2:float, lon2:float) -> float:
	'''
	Returns the distance between point A (lat1, lon1) and point B (lat2, lon2)
	As per: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
	'''
	R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km
	dLat = radians(lat2 - lat1)
	dLon = radians(lon2 - lon1)
	lat1 = radians(lat1)
	lat2 = radians(lat2)

	a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
	c = 2*asin(sqrt(a))

	return R * c

@app.route('/users/London', methods=['GET'])
def getAllUsersUnderFiftyMiles():
	# This gets us the users
	all_users = getUsers()

	# Now we need to filter out the ones not within 50 miles
	london_lat, london_long = 51.507222, -0.1275
	users_fifty_miles = list(filter(lambda person: haversine(london_lat, london_long, float(person['latitude']), float(person['longitude'])) <= 50.0, all_users))

	# Returning a json response
	return jsonify(users_fifty_miles)

if __name__ == '__main__':
	app.run(debug=False)