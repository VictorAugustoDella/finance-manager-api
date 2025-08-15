from app import create_app
from app.routes.transaction.routes import edit_transaction, view_transaction, view_transactions, create_transaction, delete_transaction
from app.models.user_transaction import Transaction, User, db
import pytest
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token



@pytest.fixture()
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
    
@pytest.fixture
def user2(client):
    with client.application.app_context():
        user = User(name='Marcos Aurelio', email='testefixture22@gmail.com', password=generate_password_hash('Senhateste4321')) 
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return user, token
    

@pytest.fixture
def transaction(client, user):
    user_obj, _ = user
    with client.application.app_context():
        t = Transaction(type='expense', amount=200, category='outros', user_id=user_obj.id)
        db.session.add(t)
        db.session.commit()
        return t.to_dict()



def test_get_success(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.get_json() == [transaction]

def test_get_type_filter_match(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?type=expense', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.get_json() == [transaction]

def test_get_amount_filter_match(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?amount=150', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.get_json() == [transaction]

def test_get_category_filter_match(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?category=ouTRos', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.get_json() == [transaction]

def test_get_category_filter_no_match(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?category=moradia', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_type_filter_invalid(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?type=trade', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 400
    assert response.get_json() == {'errors': {'type': 'Tipo invalido'}}

def test_get_amount_filter_value_invalid(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?amount=oitenta', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 400
    assert response.get_json() == {'errors': {'amount': 'Amount deve ser um número'}}

def test_get_without_token(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?amount=150')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Cabeçalho de autorização ausente'}

def test_get_invalid_token(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions?amount=150', headers={'Authorization': f'Bearer {"invalidtoken"}'})
    assert response.status_code == 422
    assert response.get_json() == {'error': 'Token inválido'}


#####
def test_get_by_id_success(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.get_json() == {'transaction': transaction}

def test_get_by_id_inexistent_transaction(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions/5', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Transação não encontrada'}

def test_get_by_id_other_user(client, user2, transaction):
    user_obj, token = user2
    
    response = client.get('/transactions/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
    assert response.get_json() == {'error': 'Transação pertencente a outro usuario'}

def test_get_by_id_without_authentication(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions/1')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Cabeçalho de autorização ausente'}

def test_get_by_id_invalid_token(client, user, transaction):
    user_obj, token = user
    
    response = client.get('/transactions/1', headers={'Authorization': f'Bearer {"invalidtoken"}'})
    assert response.status_code == 422
    assert response.get_json() == {'error': 'Token inválido'}

#####
def test_create_transaction_success(client, user, transaction):
    user_obj, token = user
    
    response = client.post('/transactions', json={"type": "expense", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert "transaction_created" in response.get_json()

def test_create_transaction_missing_camp(client, user, transaction):
    user_obj, token = user
    
    response = client.post('/transactions', json={"amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Type, amount e category devem ser obrigatorios'}

def test_create_transaction_invalid_type(client, user, transaction):
    user_obj, token = user
    
    response = client.post('/transactions', json={"type": "trade", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Tipo de transação inválido'}

def test_create_transaction_invalid_amount(client, user, transaction):
    user_obj, token = user
    
    response = client.post('/transactions', json={"type": "expense", "amount": "duzentos", "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Amount deve ser um numero maior que 0'}

def test_create_transaction_invalid_category(client, user, transaction):
    user_obj, token = user
    
    response = client.post('/transactions', json={"type": "expense", "amount": 200, "category": "freelance"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Categoria inválida'}

def test_create_transaction_without_authentication(client, user, transaction):
    user_obj, token = user
    
    response = client.post('/transactions', json={"type": "expense", "amount": 200, "category": "transporte"})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Cabeçalho de autorização ausente'}

def test_create_transaction_invalid_token(client, user, transaction):
    user_obj, token = user
    
    response = client.post('/transactions', json={"type": "expense", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {"invalidtoken"}'})
    assert response.status_code == 422
    assert response.get_json() == {'error': 'Token inválido'}


#####
def test_edit_transaction_success(client, user, transaction):
    user_obj, token = user
    
    response = client.put('/transactions/1', json={"type": "expense", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert "transaction edited" in response.get_json() 

def test_edit_transaction_inexistent(client, user, transaction):
    user_obj, token = user
    
    response = client.put('/transactions/99', json={"type": "expense", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Transação não encontrada'}

def test_edit_transaction_other_user(client, user2, transaction):
    user_obj, token = user2
    
    response = client.put('/transactions/1', json={"type": "expense", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
    assert response.get_json() == {'error': 'Você não tem permissão para acessar essa transação'}

def test_edit_transaction_missing_camp(client, user, transaction):
    user_obj, token = user
    
    response = client.put('/transactions/1', json={"amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Type, amount e category devem ser obrigatorios'}

def test_edit_transaction_invalid_type(client, user, transaction):
    user_obj, token = user
    
    response = client.put('/transactions/1', json={"type": "trade", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Tipo de transação inválido'}

def test_edit_transaction_without_authentication(client, user, transaction):
    user_obj, token = user
    
    response = client.put('/transactions/1', json={"type": "expense", "amount": 200, "category": "transporte"})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Cabeçalho de autorização ausente'}

def test_edit_transaction_invalid_token(client, user, transaction):
    user_obj, token = user
    
    response = client.put('/transactions/1', json={"type": "expense", "amount": 200, "category": "transporte"}, headers={'Authorization': f'Bearer {"invalidtoken"}'})
    assert response.status_code == 422
    assert response.get_json() == {'error': 'Token inválido'}


#####
def test_delete_transaction_success(client, user, transaction):
    user_obj, token = user
    
    response = client.delete('/transactions/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 204
    assert response.data == b''

def test_delete_transaction_inexistent(client, user, transaction):
    user_obj, token = user
    
    response = client.delete('/transactions/99', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Transação não encontrada'}

def test_delete_transaction_other_user(client, user2, transaction):
    user_obj, token = user2
    
    response = client.delete('/transactions/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
    assert response.get_json() == {'error': 'Você não tem permissão para acessar essa transação'}

def test_delete_transaction_without_authentication(client, user, transaction):
    user_obj, token = user
    
    response = client.delete('/transactions/1')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Cabeçalho de autorização ausente'}

def test_delete_transaction_invalid_token(client, user, transaction):
    user_obj, token = user
    
    response = client.delete('/transactions/1', headers={'Authorization': f'Bearer {"invalidtoken"}'})
    assert response.status_code == 422
    assert response.get_json() == {'error': 'Token inválido'}


