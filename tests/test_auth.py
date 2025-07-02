from app.routes.auth.routes import register, login, profile
from app.models.userModels import User
import pytest
from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def user(client):
    with client.application.app_context():
        user = User(name='Victor Augusto', email='testefixture@gmail.com', password=generate_password_hash('Senhateste4321')) 
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return user, token
    
def test_register_sucess(client):
    response = client.post('/register', json={"name": "Marcos Aurelio", "email": "testefixture@gmail.com", "password":"Senhateste4321"})
    assert response.status_code == 201
    assert response.get_json() == {'user adcionado': "Marcos Aurelio"}

def test_register_invalid_name(client):
    response = client.post('/register', json={"name": "Marcos 123", "email": "testefixture@gmail.com", "password":"Senhateste4321"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "User inválido"}

def test_register_invalid_email(client):
    response = client.post('/register', json={"name": "Marcos Aurelio", "email": "testefixturequebradogmail.com", "password":"Senhateste4321"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "E-mail inválido"}

def test_register_invalid_password(client):
    response = client.post('/register', json={"name": "Marcos Aurelio", "email": "testefixture@gmail.com", "password":"senhafraca"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Senha muito fraca! [Mínimo 8 caracteres, 1 letra maiúscula,  1 letra minúscula,  1 número]"}

def test_register_duplicated_email(client, user):
    response = client.post('/register', json={"name": "Marcos Aurelio", "email": "testefixture@gmail.com", "password":"Senhateste4321"})
    assert response.status_code == 409
    assert response.get_json() == {'error': 'Email ja registrado'}

def test_register_without_camp(client):
    response = client.post('/register', json={"name": "Marcos Aurelio", "password":"Senhateste4321"})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Todos os campos são obrigatórios'}
    

