from flask import Flask, request, jsonify
from . import transaction_bp
from ...models.userModels import User, Transaction, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

@transaction_bp.route('/transactions', methods=['GET'])
@jwt_required()
def view_transactions():
    user_id = int(get_jwt_identity())

    transaction_obj = Transaction.query.filter_by(user_id=user_id)

    error={}

    type = request.args.get('type')
    amount = request.args.get('amount')
    category = request.args.get('category')
    date = request.args.get('date')

    if type is not None:
        if type not in ['income', 'expense', 'refund']:
            error['type'] = 'Tipo invalido'
        transaction_obj= transaction_obj.filter_by(type=type)

    if amount is not None:
        try:
            amount = float(amount)
            if amount < 0:
                error['amount'] = 'Amount deve ser maior ou igual a 0'
        except ValueError:
            error['amount'] = 'Amount deve ser um número'
        
        transaction_obj = transaction_obj.filter(Transaction.amount >= amount)
                
    if category is not None:
        transaction_obj = transaction_obj.filter_by(category=category)

    if error:
        return jsonify({'errors': error}), 400


    return jsonify([t.to_dict() for t in transaction_obj.all()]), 200


@transaction_bp.route('/transactions/<int:id>', methods=['GET'])
@jwt_required()
def view_transaction(id):
    user_id = int(get_jwt_identity())

    transaction_obj = Transaction.query.get(id)

    if not transaction_obj:
        return jsonify({'error': 'task não encontrada'}), 404

    if transaction_obj.user_id != user_id:
        return jsonify({'error': 'task pertencente a outro usuario'}), 403

    return jsonify({'transaction': transaction_obj.to_dict()}), 200
    