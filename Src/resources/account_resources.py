from flask_restful import Resource

def register_account_resources(api):
    api.add_resource(AccountResource, '/api/accounts')

class AccountResource(Resource):
    def get(self):
        return {'message': 'Account endpoint placeholder'}, 200 