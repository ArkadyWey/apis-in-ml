# apis_in_ml

FastAPI demo for MLE fellowship

## Instructions
### 1. Clone the repository.
```
git clone https://gitlab.com/facultyai/fellowship/mle-fellowship-teaching-resources/apis-in-ml.git
```

### 2. Understand the structure of the repository.
Review the files and their contents.

### 3. Create the virtual environment, install the dependencies and activate it.
```
poetry install
poetry shell
```

### 4. Add `fastapi` to the virtual environment.
```
poetry add fastapi
```
Observe the libraries talked about earlier (starlette, pydantic) being installed.

### 5. Add `uvicorn` to the virtual environment.

### 6. Run the server & review the response in the browser.
```
cd src/apis_in_ml
uvicorn main:app --reload
```

### 7. Send a request to the API to retrieve a participant from the database.
Try with the `participant_id=1` and `participant_id=2`. What responses does they API return?
Send a request using the Swagger docs (`localhost:8000/docs`), `curl` and Postman.

### 8. Add an endpoint to the API to add a participant to the database.
The database code has been written already.

### 9. Add a test for the new endpoint.
Use the examples provided for guidance.

### 10. Add `fastapi_auth_middleware` to the virtual environment.
```
poerty add fastapi_auth_middleware
```

### 11. Add Authenication middleware to restrict only admins from adding participants and only super users from deleting participants.
Use [this](!https://fastapi-auth-middleware.code-specialist.com/) as a guideline.
Middleware: Tool for processing requests and responses before they reach endpoint logic or afterwards.

### 12. Add two new endpoints to the API to interact with the TextClassification model. 
a. The first endpoint should accept a classication input (see `ClassificationInput` in `src/apis_in_ml/models.py`), add a background task to run the text classification using `TextClassifier` in `src/apis_in_ml/classifier.py` and return a response with a message including the `run_id`. 

b. The second endpoint should accept a `run_id` and query the database to see if the run has successfully completed. If a result exists, it should be returned. Otherwise, return a message saying it is yet to be completed.

Make use of FastAPIs [background](https://fastapi.tiangolo.com/tutorial/background-tasks/) tasks to do this.
The model will need to be unzipped (manually or otherwise).

### 13. Use the instructions in the Dockerfile to run your app using Docker.