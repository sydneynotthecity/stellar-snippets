# Stellar Coding Challenge

### Design Decisions
For ease of use, I selected the python Flask web application framework. Flask works well for REST APIs when no user interface is necessary. I decided to break out the snippet saving and fetching into two routes so that the methods were isolated. I used a SimpleCache to cache the data and enabled a timeout on the cache so that the route would expire.

### Assumptions
* API does not need to be session specific. Regardless of user, all snippets and names will be saved to the cache.
* There is no need for a global timeout for the snippets. If a user requested a `name` every 30 seconds,
the API would continue to return the `snippet`.
* API does not need security or user authentication (this is a bad assumption)
* It is ok for a snippet name to be overwritten (they should not be immutable)
* API only runs locally (needs to be deployed and hosted on a external web server)

### Error Handling and Production concerns
`Marshmallow` was used to perform schema validation on the incoming request body. The developer can define a schema (request names, data types, whether the field is required) and Marshmallow will validate and return errors if the request is ill formatted. Marshmallow performed the Error Handling for the request.


Additional Error Handling would be security/authentication if given the time.

### Testing

To test the API, pull the code locally. This API uses `virtualenv` to manage dependencies within the app.
If you do not have virtualenv, please download the package by running `pip install virtualenv`. Once installed,
run the following commands from a terminal window (MacOS or Linux):

1. Navigate inside the project: `cd path/to/stellar-webserver`
2. Create and activate a virtual env based on `requirements.txt`: `source env/bin/activate`
3. Start the Webserver: `python api/api.py`
4. In another terminal window, run the tests: `./test/test.sh`

Ideally there would be unit tests and integration tests (using karate or readyAPI) before a production deployment to ensure
adequate test coverage. I prioritized getting a working API before testing more than the required tests.
