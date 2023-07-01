# Receipt Processing API - Fetch

This is a Python-based API for processing receipts and calculating points based on specific rules. It provides several endpoints for interacting with the API.

## Prerequisites

- Python 3.9 or above
- Docker (optional)

## Installation

To run the API locally, follow these steps:

1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
4. Start the API server using the following command:
   ```
   uvicorn main:app --reload
   ```
   The API will be accessible at http://localhost:8000.

Alternatively, you can use Docker to build and run the API:

1. Build the Docker image using the provided Dockerfile:
   ```
   docker build -t receipt-api .
   ```
2. Run a Docker container using the built image:
   ```
   docker run -d --name receipt-api-container -p 8000:80 receipt-api
   ```
   The API will be accessible at http://localhost:8000.

## API Endpoints

### Get Points by ID

- **URL**: `/receipts/{id}/points`
- **Method**: GET
- **Description**: Retrieves the points associated with a specific receipt ID.
- **Query Parameters**:
  - `id` (string): The unique identifier of the receipt.
- **Response**:
  - `points` (integer): The calculated points for the receipt ID.
- **Example**:
  ```
  GET /receipts/12345/points
  Response: {"points": 50}
  ```

### Get All Receipt IDs

- **URL**: `/receipts/ids`
- **Method**: GET
- **Description**: Retrieves all receipt IDs along with their associated information.
- **Response**:
  - List of objects containing the following fields:
    - `id` (string): The unique identifier of the receipt.
    - `receipt` (object): The receipt details.
    - `points` (integer): The calculated points for the receipt.
- **Example**:
  ```
  GET /receipts/ids
  Response: [{"id": "12345", "receipt": {...}, "points": 50}, {"id": "67890", "receipt": {...}, "points": 75}]
  ```

### Process Receipt

- **URL**: `/receipts/process`
- **Method**: POST
- **Description**: Processes a receipt by calculating the associated points.
- **Request Body**:
  - `receipt` (object): The receipt details including retailer, purchase date, purchase time, total, and items.
    - `retailer` (string): The name of the retailer.
    - `purchaseDate` (string): The date of purchase (format: "YYYY-MM-DD").
    - `purchaseTime` (string): The time of purchase (format: "HH:MM").
    - `total` (string): The total amount of the receipt.
    - `items` (array): An array of objects representing the purchased items.
      - `shortDescription` (string): The short description of the item.
      - `price` (string): The price of the item.
- **Response**:
  - `id` (string): The unique identifier assigned to the processed receipt.
- **Example**:
  ```
  POST /receipts/process
  Request Body: {"retailer": "Example Retailer", "purchaseDate": "2023-06-30", "purchaseTime": "15:30", "total": "20.50", "items": [{"shortDescription": "Item 1", "price": "10.00"}, {"shortDescription": "Item 2", "price": "5.25"}]}
  Response: {"id": "12345"}
  ```

## API - Hosted

The api is also hosted. The endpoints can be accessed through the link: https://fecth-api.onrender.com/
As the API uses FastAPI library the enpoints can be tested using the link: https://fecth-api.onrender.com/docs. No local setup is required.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to contribute and enhance the functionality of this API.