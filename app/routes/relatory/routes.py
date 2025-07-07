from flask import Flask, request, jsonify
from . import relatory_bp
from ...models.userModels import User, Transaction, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ...models.categories import VALID_CATEGORIES
from ...utils.validators import validator_amount, normalize_str, is_valid_month

@relatory_bp.route('/summary')
@jwt_required()
def relatory_monthly():
    
    month = normalize_str(request.args.get('month'))

    if month and not is_valid_month(month):
        return jsonify({'error': 'Parâmetro "month" inválido. Use o formato YYYY-MM'}), 400
    
    start_date =f"{month}-01"
    end_date = f"{month}-31"
    

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

    total_expense = sum(category_sums.values())
    category_percentages ={
        category: round((val / total_expense) * 100, 2) for category, val in category_sums.items()
    }

    return jsonify({'income': income_total,
                    'expense': expense_total,
                    'balance': balance,
                    'total expense': total_expense,
                    'category percentages': category_percentages})