from flask import Blueprint, request, jsonify
from models import db, User, Product, Order

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

@api_blueprint.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'quantity': product.quantity,
            'farmer': product.farmer.name
        }
        output.append(product_data)
    return jsonify(output)

@api_blueprint.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    product = Product.query.filter_by(id=data['product_id']).first()
    if product:
        total_price = product.price * data['quantity']
        new_order = Order(
            product_id=product.id,
            quantity=data['quantity'],
            total_price=total_price,
            customer_name=data['customer_name'],
            customer_address=data['customer_address']
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order placed successfully'}), 201
    return jsonify({'message': 'Product not found'}), 404
