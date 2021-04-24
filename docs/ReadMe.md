# Read Me
## What's done
- The intention of the code is to meet the requirement as specified in docs/PythonTest.txt
- The code is developed using Python 3.9 using Virtual environment for package isolation
- The application is build using Flask (Other dependencies are in requirements.txt)

## Pre-requisites  
- The application has a pre-requisite of MongoDB Daemon
- The mongodb uri is set as env var named connection_string(mongodb://localhost:27017/)
-The key for for obtaining jwt token is stored as key in the end

## Running
- The application's entry point is startup.py
- The command is `python main.py`
  

## Integration Tests
- The integration tests are available as a post man collection (2.1 version)
- The collection can be found at docs/IntegrationTest.postman_collection.json

## To be Done
-The status code implemented is not as per REST convention
-Here all successful response has 200, invalid request 400 and the remaining 500
-Unit test needs to be done
