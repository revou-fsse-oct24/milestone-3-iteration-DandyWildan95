from flask_restful import Resource

def register_transaction_resources(api):
    api.add_resource(TransactionResource, '/api/transactions')

def register_additional_resources(api):
    api.add_resource(AdditionalResource, '/api/transactions/additional')

class TransactionResource(Resource):
    def get(self):
        return {'message': 'Transaction endpoint placeholder'}, 200

class AdditionalResource(Resource):
    def get(self):
        return {'message': 'Additional transaction endpoint placeholder'}, 200