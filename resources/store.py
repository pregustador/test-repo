from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json() # transform in json because comes as an object
        return {'message': 'A store not found with name {}'.format(name)}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'an error occurred while inserting the store'}, 500
        return store.json(), 201 # 200 means: it's OK ! 201 means: it was creared ! I need the item because is format dict (it seems Json)

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message':'Store {} deleted'.format(name)}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]} # list comprehension
