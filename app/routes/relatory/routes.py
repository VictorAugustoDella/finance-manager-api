from flask import Flask, request, jsonify
from . import relatory_bp
from ...models.user_transaction import User, Transaction, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ...models.categories import VALID_CATEGORIES
from ...utils.validators import validator_amount, normalize_str, is_valid_month

@relatory_bp.route('/relatory')
@jwt_required()
def relatory_monthly():
    
    month = normalize_str(request.args.get('month'))

    if month and not is_valid_month(month):
        return jsonify({'error': 'Parâmetro "month" inválido. Use o formato YYYY-MM'}), 400
    
    if month != None and month != '':
        start_date =f"{month}-01"
        end_date = f"{month}-31"
    
    else:
        start_date = "0000-01"
        end_date = "2125-31"
    

    transactions= Transaction.query.filter(
        Transaction.user_id == int(get_jwt_identity()),
        Transaction.date.between(start_date, end_date)
        ).all()

    income_total = sum(t.amount for t in transactions if t.type == 'income')
    expense_total = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income_total - expense_total

    category_sums = {}
    for t in transactions:
        if t.type == 'expense':
            category = t.category
            category_sums[category] = category_sums.get(category, 0) + t.amount
    
    category_percentages ={
        category: round((val / expense_total) * 100, 2) for category, val in category_sums.items()
    }

    type_sumary = {}

    return jsonify({'income': income_total,
                    'expense': expense_total,
                    'balance': balance,
                    'expense by categorie': category_sums,
                    'category percentages': category_percentages}), 200