# bpdts-test-app
Technical test for the DWP wherin I develop a REST API that gets users from another API, an API that can list users in the UK, and displays all the users within a 50-mile radius.

# The overall structure of the program/algorithm
1) You send a get request to the API that I have written
2) This calls the REST API at https://bpdts-test-app.herokuapp.com to get all the users (via a GET request more specifically from https://bpdts-test-app.herokuapp.com/users) in a json format. 
3) Finally, we return all the users that are within a 50-mile radius of London (we assume the coordinates are '51.507222, -0.1275' as per Wikipedia) using the Haversine formula. 

# Dependencies
This application was written and tested on Ubuntu 18.04. 
This REST API depends on the following Python-3 modules:
- virtualenv
- Flask
- requests
- json