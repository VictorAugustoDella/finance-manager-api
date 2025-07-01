from flask import Flask, request, jsonify
from . import transaction_bp
from ...models.userModels import User, Transaction, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

@transaction_bp.route('/transactions', methods=['GET'])
def view_transaction():
    user_id = int(get_jwt_identity())

    transaction_obj = Transaction.query.filter_by(user_id=user_id)

    type = request.args.get('type')
    amount = request.args.get('amount')
    category = request.args.get('category')
    date = request.args.get('date')
    if 

    return jsonify([t.to_dict() for t in transaction_obj.all()]), 200