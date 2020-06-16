# bpdts-test-app
Technical test for the DWP wherein I develop a REST API that gets users from another API, an API that can list users in the UK, and displays all the users within a 50-mile radius.

# The overall structure of the program/algorithm
1) You send a get request to the API that I have written
2) This calls the REST API at https://bpdts-test-app.herokuapp.com to get all the users (via a GET request more specifically from https://bpdts-test-app.herokuapp.com/users) in a json format. 
3) Finally, we return all the users that are within a 50-mile radius of London (we assume the coordinates are '51.507222, -0.1275' as per Wikipedia) using the Haversine formula. 

# Dependencies
This application was written and tested on Ubuntu 18.04. 
This REST API depends on the following Python-3.6 modules:
- virtualenv
- Flask
- requests

# Running the application
After cloning the project using:
> git clone <the hash of this project>

Install the dependencies using but running the command in terminal:
> chmod a+x install_dependencies.sh

> ./install_dependencies.sh

Create a server on localhost using first changing the execution permissions of app.py by:
> chmod a+x app.py

And then actually running the application:
> ./app.py

You can send commands to the API via writing commands in the terminal. To get all the people within a 50-mile radius of London, use:
>  curl -i "http://localhost:5000/users/London"

Similarly, you can get all the people within a 50-mile radius of a generic latitude and longitude (this was done as some people may slightly disagree with the latitude, longitude I've assumed) via the command:
> curl -i "http://localhost:5000/users/London?latitude=x&longitude=y"

where x and y are the latitude (a "float") and longitude (also a "float") respectively

# Testing
Run unit tests created using the command: 
> python3 -m unittest tests.tests
