from flask import Flask, request, jsonify
from . import auth_bp
from ...models.userModels import User, Transaction, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ...utils.validators import is_valid_email, is_valid_full_name, is_valid_password


@auth_bp.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')


    #Verificando se foram passados os dados pedidos
    if not name or not email or not password:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    name = name.strip()
    email = email.strip().lower()
    
    if not is_valid_full_name(name):
        return jsonify({"error": "User inválido"}), 400
    
    if not is_valid_email(email):
        return jsonify({"error": "E-mail inválido"}), 400
 
    if not is_valid_password(password):
        return jsonify({"error": "Senha muito fraca! [Mínimo 8 caracteres, 1 letra maiúscula,  1 letra minúscula,  1 número]"}), 400
    

    #Verificando se possui um usuario ja cadastrado com esse nome
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email ja registrado'}), 409
    
    newuser = User(name=name, email=email, password=generate_password_hash(password))

    db.session.add(newuser)
    db.session.commit()

    return jsonify({'user adcionado': name}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    email = email.strip().lower()

    user_obj = User.query.filter_by(email=email).first()

    if user_obj and check_password_hash(user_obj.password, password):
        access_token = create_access_token(identity=str(user_obj.id))
        return jsonify(access_token=access_token), 200
    return jsonify({'error': 'Email ou senha incorretos'}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())

    user_obj = User.query.get(user_id)

    if not user_obj:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    return jsonify(user_obj.to_dict()), 200

