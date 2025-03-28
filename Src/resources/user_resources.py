from flask_restful import Resource

def register_user_resources(api):
    api.add_resource(UserResource, '/api/users')

class UserResource(Resource):
    def get(self):
        return {'message': 'User endpoint placeholder'}, 200