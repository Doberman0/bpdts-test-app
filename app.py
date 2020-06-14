#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request # Allows us to take multiple arguments
import requests # To get users from API provided
import json
from math import radians, cos, sin, asin, sqrt
from typing import List


app = Flask(__name__)

# -------------------------   Helper functions -------------------------

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

# -------------------------- Main code ---------------------------------

# You can call this function using the get method at http://localhost:5000/users/London
# Structured this way as you may later want to extend the API to include other functionality
@app.route('/users/London', methods=['GET'])
def getAllUsersUnderFiftyMiles() -> List[dict]:
	''' This allows us to alter where we're searching from generalising the API
		This is advantageous as some people may use slightly different coordinates for London
		and this gives them that flexibility. Will default to (51.507222, -0.1275) for 
		the latitude and longitude respectively if no values are provided in the request
	'''
	london_lat = request.args.get('latitude', 51.507222)
	london_long =  request.args.get('longitude', -0.1275)

	# This gets us the users from https://bpdts-test-app.herokuapp.com
	all_users = getUsers()

	# Now we need to filter out the ones not within 50 miles
	max_distance = 50.0 # The maximum distance from London, 50 miles
	users_fifty_miles = list(filter(lambda person: haversine(london_lat, london_long, float(person['latitude']), float(person['longitude'])) <= max_distance, all_users))

	# Returning a json response
	return jsonify(users_fifty_miles)

# Starting the application/service
if __name__ == '__main__':
	app.run(debug=False)