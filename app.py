from flask import Flask, jsonify
from uuid import uuid4
from flask_pydantic import validate
from serializer import OrderSerializer, COMPONENTS

# Initialize Flask app
app = Flask(__name__)

# API endpoint to create a new order
@app.route('/orders', methods=['POST'])
@validate(body=OrderSerializer)
def create_order(body: OrderSerializer):
    """Create a new mobile order."""
    try:
        # Validate the request body and extract components list
        data = body.model_dump()
        components = data.get('components')

        # Calculate total order cost
        total = sum(COMPONENTS[code].price for code in components)
        
        # Get part names
        parts = [COMPONENTS[code].name for code in components]

        # Create order response
        order_response = {
            'order_id': str(uuid4()),
            'total': round(total, 2),
            'parts': parts
        }

        return jsonify(order_response), 201
    except Exception as e:
        return jsonify({'error': "Error creating order: " + str(e)}), 400

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all errors and exceptions."""
    return jsonify({'error': str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)