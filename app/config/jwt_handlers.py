from flask import jsonify

def setup_jwt_handlers(jwt):

    @jwt.unauthorized_loader
    def custom_unauthorized_response(err_str):
        return jsonify({'error': 'Cabeçalho de autorização ausente'}), 401
    
    @jwt.invalid_token_loader
    def custom_invalid_token_response(err_str):
        return jsonify({'error': 'Token inválido'}), 422
    
    @jwt.expired_token_loader
    def custom_expired_token_response(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expirado'}), 401