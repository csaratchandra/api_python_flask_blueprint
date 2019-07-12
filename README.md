# api_python_flask_blueprint
API implementation using python, flask and blueprint

## Pre-requisites
    - Python 3.7 has been used and same is required for running this.
       Python and most of the supporting libraries are installed via [anaconda distribution](https://www.anaconda.com/distribution/#download-section)
     - requirements.txt contains list of all the libraries installed in the dev environment.
    Install the libraries using ```pip install -r requirements.txt``` in the app folder.
    (Please note some of the libraries may not be required but have been included to avoid any issues)

## To Execute the code
    * Once libraries are installed as stated above, proceed with below steps:
    - Open terminal/bash console
    - Change to api_python_flask_blueprint/
    - From within the above folder type ```flask run``` to start the flask server

## Sample API URLs
    - To view transaction summary at city level for last 10 days
    http://127.0.0.1:8080/assignment/transactionSummaryByManufacturingCity/10

    - To view transaction summary at product level for last 5 days
    http://127.0.0.1:8080/assignment/transactionSummaryByProducts/5

    - To view transaction information for each individual transaction id
    http://127.0.0.1:8080/assignment/transaction/2
    
## Implementation Overview:
   Code has been divied into two modules using **flask_blueprint**:

### 1) Contains implementation of 3 APIs using HTTP GET verb
   Code is present in app_api/app/api/
   Below are the 3 APIs, implemented in transaction.py 
 1) ​http://localhost:8080/assignment/transaction​/{transaction_id}
 2) http://localhost:8080/assignment/transactionSummaryByProducts​/{last_n_days}
 3) http://localhost:8080/assignment/transactionSummaryByManufacturingCity​/{last_n_days}


### 2) Very basic error handling
  Code is present in app_api/app/errors, error handling is basic as error handling specifc to APIs is also present in that specific module.
  
### Future Improvements:
  - This code takes input data from a folder which is the landing folder for streaming content. In future, a script can be created to segregate landing folder and app input folder.
  - Currently when there is an error, HTTP error codes are sent in response. Custom error codes can be added to the code to give more detailed error information.
  - Logging can also be added.
