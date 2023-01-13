This code provides a rest end point that interfaces with another API and returns some calculated data.

To run this code:

- Clone the repository
- Make sure you have docker installed
- Run make build to create the docker image
- Run make run to run the container with the server running on port 8081

To use the api do the following:

- curl "http://localhost:8081/settlement/?merchant_id=<merchant_id>&date=<date>"
- merchant_id is the id of the merchant in string format
- date is in the format yyyy-mm-dd
- The api will return the merchant_id, date, and the net settlement amount for the given date
