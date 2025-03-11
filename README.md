# Mobile Factory API

This is a Flask-based API for creating mobile phone orders with given specifications.

## Setup

1. Clone/Download the repository

2. Navigate to the project directory
`cd mobile-factory-api`

3. Install dependencies
`pip install -r requirements.txt`

4. Run the application
`python app.py`

5. Access the API at `http://localhost:5000/orders`.
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"components": ["I", "A", "D", "F", "K"]}' \
http://localhost:5000/orders
```


## To test the API endpoint
`python -m unittest tests.py -v`

### Approach
The API is built using Flask and Pydantic for data validation. 

It's a POST request to `/orders` endpoint with a JSON payload containing a list of component codes.

### Components
- A: LED Screen
- B: OLED Screen
- C: AMOLED Screen
- D: Wide-Angle Camera
- E: Ultra-Wide-Angle Camera
- F: USB-C Port
- G: Micro-USB Port
- H: Lightning Port
- I: Android OS
- J: iOS OS
- K: Metallic Body
- L: Plastic Body

### Example
```json
{
    "components": ["A", "D", "F", "I", "K"]
}
```

### Response
```json
{
    "order_id": "123e4567-e89b-12d3-a456-426614174000",
    "total": 131.61,
    "parts": ["LED Screen", "Wide-Angle Camera", "USB-C Port", "Android OS", "Metallic Body"]
}
```
