from app.routes.auth.routes import register, login, profile
from app.models.user_transaction import User
import pytest
from os import getenv

from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


@pytest.fixture
def client():

    test_db_url = getenv("TEST_DATABASE_URL", "sqlite:///:memory:")

    app = create_app(database_uri=test_db_url)
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret'

    with app.app_context():
        db.create_all()
        client = app.test_client()
        yield client
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
    

def test_login_success(client, user):
    response = client.post('/login', json={"email": "testefixture@gmail.com", "password":"Senhateste4321"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_wrong_email(client, user):
    response = client.post('/login', json={"email": "testefixture222@gmail.com", "password":"Senhateste4321"})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Email ou senha incorretos'}

def test_login_wrong_password(client, user):
    response = client.post('/login', json={"email": "testefixture@gmail.com", "password":"1234etsetahneS"})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Email ou senha incorretos'}

def test_login_without_email(client, user):
    response = client.post('/login', json={ "password":"Senhateste4321"})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Email e senha são obrigatórios'}

def test_login_without_password(client, user):
    response = client.post('/login', json={"email": "testefixture@gmail.com"})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Email e senha são obrigatórios'}

def test_login_normalization_email(client, user):
    response = client.post('/login', json={"email": " tEstEfiXTurE@gMAIl.com  ", "password":"Senhateste4321"})
    assert response.status_code == 200


def test_profile_success(client, user):
    user_obj, token = user
    response = client.get('/profile', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.get_json() == user_obj.to_dict()

def test_profile_without_token(client, user):
    response = client.get('/profile')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Cabeçalho de autorização ausente'}

def test_profile_invalid_token(client, user):
    response = client.get('/profile', headers={
        'Authorization': f'Bearer invalidtoken123123'
    })
    assert response.status_code == 422
    assert response.get_json() == {'error': 'Token inválido'}

def test_profile_user_inexistent(client, user):
    user_obj, token = user
    db.session.delete(user_obj)
    db.session.commit()
    response = client.get('/profile', headers={
        'Authorization': f'Bearer {token}'
    }) 
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Usuário não encontrado'}
