<h1 align="center">💼 Finance Manager API</h1>

<p align="center">
  Uma API RESTful de gerenciamento de transações financeiras com autenticação JWT, validações robustas e testes automatizados.<br>
  Ideal para uso como backend de aplicativos de controle financeiro pessoal, gestão de despesas ou orçamentos.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Flask-3.1.0-lightgrey?style=flat-square&logo=flask" />
  <img src="https://img.shields.io/badge/FlaskSQLAlchemy-3.1.1-ff6347?style=flat-square" />
  <img src="https://img.shields.io/badge/Pytest-Testes-6c5ce7?style=flat-square" />
</p>

<hr>

---

## 🌐 URL de Deploy

A API está disponível no Render:

[https://finance-manager-api-namz.onrender.com](https://finance-manager-api-namz.onrender.com)

---

## 🧰 Tecnologias Utilizadas

- [Flask](https://flask.palletsprojects.com/) — microframework web em Python
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM para banco de dados
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) — autenticação com JWT
- [Werkzeug](https://werkzeug.palletsprojects.com/) — utilitários para segurança
- [Pytest](https://docs.pytest.org/) — testes automatizados

---

## 🛠️ Instalação e Execução Local (Opcional)


 ### 1. Clone o repositório
 ```bash
git clone https://github.com/victoraugustodella/finance-manager-api.git
cd finance-manager-api
```
### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
venv\Scripts\activate  # ou source venv/bin/activate no Linux/Mac
```
### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
### 4. Rode a aplicação
```bash
python run.py
```
---
## ⚙️ Variáveis de Ambiente (Render)

#### Não é necessário .env no Render, configure no painel:

DATABASE_URL → URL do Postgres do Render

SECRET_KEY → chave do Flask

JWT_SECRET_KEY → chave JWT

#### Exemplo local opcional:

```env
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=jwt-dev-key
```

---
## 📬 Rotas
### 🔐 Auth

| Método | Rota        | Descrição              |
| ------ | ----------- | ---------------------- |
| POST   | `/register` | Registra novo usuário  |
| POST   | `/login`    | Gera token JWT         |
| GET    | `/profile`  | Retorna usuário logado |

### 💲 Transaction

| Método | Rota                  | Descrição                         |
| ------ | --------------------- | --------------------------------- |
| GET    | `/transactions`       | Lista todas as transações do user |
| GET    | `/transactions/<id>`  | Detalha uma transação específica  |
| POST   | `/transactions`       | Cria nova transação               |
| PUT    | `/transactions/<id>`  | Edita uma transação               |
| DELETE | `/transactions/<id>`  | Remove uma transação              |

### 📈 Relatory

| Método | Rota                      | Descrição                                     |
| ------ | ------------------------- | --------------------------------------------- |
| GET    | `/relatory`               | Retorna um resumo financeiro geral do usuário |
| GET    | `/relatory?month=2025-07` | Retorna o resumo financeiro de julho de 2025  |

---

## 📬 Testando no Postman / Thunder Client

Para testar a API, você precisa configurar **Headers e Body** corretamente.

- Para comecar, faca um POST no `/register` com JSON:

```json
{
  "name": "seu_nome seu_sobrenome",
  "email": "seu_email",
  "password": "sua_senha"
}
```

### 🔐 Autenticação JWT

- Todas as rotas de transações e relatórios requerem JWT no cabeçalho.
- Header:

| Key           | Value                  |
| ------------- | ---------------------- |
| Authorization | Bearer <seu_token_jwt> |

- Obtenha o token fazendo POST no `/login` com JSON:

```json
{
  "email": "seu_email",
  "password": "sua_senha"
}
```

- Resposta esperada:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

### Criar Transação (/transactions)
- Headers:

| Key           | Value                     |
| ------------- | ------------------------- |
| Authorization | Bearer \<seu\_token\_jwt> |

- Body (JSON):

```json
{
  "amount": 1200,
  "category": "Moradia",
  "type": "expense",
}
```
- Resposta esperada:
201 Created + JSON da transação criada


---

## 📁 Estrutura de Pastas
```bash
finance-manager-api/
│
├── app/
│   ├── config/
│   │   └── jwt_handlers.py       # Handlers personalizados de erro do JWT
│   │   
│   ├── models/
│   │   ├── user_transaction.py   # Models: User e Transaction + método to_dict()
│   │   └── categories.py         # Dicionário com categorias válidas de transações por tipo
│   │
│   ├── routes/
│   │   ├── auth/
│   │   │   ├── __init__.py       # Blueprint de autenticação
│   │   │   └── routes.py         # Rotas: /register, /login, /profile
│   │   ├── relatory/
│   │   │   ├── __init__.py       # Blueprint de relatório
│   │   │   └── routes.py         # Rotas: /relatory
│   │   └── transaction/
│   │       ├── __init__.py       # Blueprint de transações
│   │       └── routes.py         # Rotas: /transactions CRUD completo
│   │   
│   ├── utils/
│   │   └── validators.py         # Validações customizadas
│   │  
│   └── __init__.py               # Função create_app com registradores e configs
│
├── tests/
│   ├── test_auth.py              # Testes para autenticação (login, register, me)
│   └── test_transaction.py       # Testes para as transações (CRUD e filtros)
│
├── db.py                         # Instância do SQLAlchemy
├── README.md                     # Documentação do projeto
├── requirements.txt              # Dependências do projeto
└── run.py                        # Ponto de entrada da aplicação
```

## 🧪 Testes
O projeto possui cobertura de testes automatizados com Pytest.
```bash
# Rode todos os testes
pytest
```
### Testes cobrem:
- Cadastro, login e autenticação
- CRUD de transações
- Erros esperados (401, 403, 404, etc)

# Observação
Atualmente, os testes são configurados para usar **exclusivamente** o **SQLite** em memória e não interagem com o banco de dados PostgreSQL principal. Isso garante que os testes sejam rápidos e não modifiquem seus dados reais.

## ✨ Contribuição
Achou um bug? Quer ajudar?
Sinta-se livre para abrir uma [issue](https://github.com/VictorAugustoDella/finance-manager-api/issues) ou enviar um Pull Request!

## 📄 Licença
Esse projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://github.com/VictorAugustoDella/finance-manager-api/blob/main/LICENSE) para mais detalhes.
```yaml
MIT License

Copyright (c) 2025 VictorAugustoDella

Permission is hereby granted, free of charge, to any person obtaining a copy...
```
---

<h3 align="center">
  Feito com amor ❤️ por <a href="https://github.com/VictorAugustoDella"><b>Victor Augusto</b></a>
</h3>
