from flask import Flask, request, jsonify
from . import transaction_bp
from ...models.userModels import User, Transaction, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ...models.categories import VALID_CATEGORIES
from ...utils.validators import validator_amount, normalize_str

all_categories = [normalize_str(cat) for cat in VALID_CATEGORIES['income'] + VALID_CATEGORIES['expense']]

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
        transaction_obj = transaction_obj.filter_by(category=normalize_str(category))

    if error:
        return jsonify({'errors': error}), 400


    return jsonify([t.to_dict() for t in transaction_obj.all()]), 200


@transaction_bp.route('/transactions/<int:id>', methods=['GET'])
@jwt_required()
def view_transaction(id):
    user_id = int(get_jwt_identity())

    transaction_obj = Transaction.query.get(id)

    if not transaction_obj:
        return jsonify({'error': 'Transação não encontrada'}), 404

    if transaction_obj.user_id != user_id:
        return jsonify({'error': 'Transação pertencente a outro usuario'}), 403

    return jsonify({'transaction': transaction_obj.to_dict()}), 200


@transaction_bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():

    data = request.get_json()
    user_id = int(get_jwt_identity())


    vtype = data.get('type')
    amount = data.get('amount')
    category = normalize_str(data.get('category'))


    if not all([category, vtype]) or amount is None:
        return jsonify({'error': 'Type, amount e category devem ser obrigatorios'}), 400

    
    if vtype not in ['income', 'expense', 'refund']:
        return jsonify({'error': 'Tipo de transação inválido'}), 400
    
    if not validator_amount(amount):
        return jsonify({'error': 'Amount deve ser um numero maior que 0'}), 400
        
    
    if category not in all_categories:
        return jsonify({'error': 'Categoria inválida'}), 400
    
    
    
    transaction = Transaction(user_id=user_id, type=vtype, amount=float(amount), category=category)
    
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'trancation_created': transaction.to_dict()}), 201


@transaction_bp.route('/transactions/<int:id>', methods=['PUT'])
@jwt_required()
def edit_transaction(id):
    data = request.get_json()
    user_id = int(get_jwt_identity())
    
    transaction_obj = Transaction.query.get(id)


    if not transaction_obj:
        return jsonify({'error': 'Transação não encontrada'}), 404

    if transaction_obj.user_id != user_id:
        return jsonify({'error': 'Você não tem permissão para acessar essa transação'}), 403
    
    vtype = data.get('type')
    amount = data.get('amount')
    category = normalize_str(data.get('category'))


    if not all([category, vtype]) or amount is None:
        return jsonify({'error': 'Type, amount e category devem ser obrigatorios'}), 400

    
    if vtype not in ['income', 'expense', 'refund']:
        return jsonify({'error': 'Tipo de transação inválido'}), 400
    
    if not validator_amount(amount):
        return jsonify({'error': 'Amount deve ser um numero maior que 0'}), 400
        
    
    if category not in all_categories:
        return jsonify({'error': 'Categoria inválida'}), 400
    
    transaction_obj.type = vtype
    transaction_obj.amount = float(amount)
    transaction_obj.category = category

    db.session.commit()

    return jsonify({'transaction edited': transaction_obj.to_dict()}), 200

    