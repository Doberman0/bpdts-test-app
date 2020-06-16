#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request # Allows us to take multiple arguments
from flask import make_response
from flask import abort
from typing import List
from helper_functions import getUsers
from helper_functions import haversine


app = Flask(__name__)

@app.route('/users/London', methods=['GET'])
def getAllUsersUnderFiftyMiles() -> List[dict]:
	'''
	You can call this function using the get method at http://localhost:5000/users/London
	This returns all users 50 or fewer miles from London
	'''

	# This allows us to alter where we're searching from generalising the API
	# This is advantageous as some people may use slightly different coordinates for London
	# and this gives them that flexibility. Will default to (51.507222, -0.1275) for 
	# the latitude and longitude respectively if no values are provided in the request
	# For different parameters, use curl -i "http://localhost:5000/users/London?latitude=x&longitude=y"
	try:
		london_lat = float(request.args.get('latitude', 51.507222))
		london_long =  float(request.args.get('longitude', -0.1275))
	except ValueError:
		# Throw an error 404 if the user enters an non-float/integer for latuitude/longitude
		abort(404)

	# This gets us the users from https://bpdts-test-app.herokuapp.com
	all_users = getUsers()

	# Now we need to filter out the ones not within 50 miles
	max_distance = 50.0 # The maximum distance from London, 50 miles
	users_fifty_miles = list(filter(lambda person: haversine(london_lat, london_long, float(person['latitude']), float(person['longitude'])) <= max_distance, all_users))

	# Returning a json response
	return jsonify(users_fifty_miles)

#We make our own error handler to return a json response
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'Error': 'Please enter numerical values'}), 404)

# Starting the application/service
if __name__ == '__main__':
	app.run(debug=False)