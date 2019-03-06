import sqlite3
from flask_jwt import jwt_required # JWT is Jason Web Token
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    # The case below 'price' is required (I put it in Postman body tag...)
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item needs store_id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() # transform in json because comes as an object
        return {'message': 'item not found'}, 404

    # for production site is recommended put jwt_required() in some http verbs like this one bellow
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'mesage': "An item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        # item = ItemModel(name, data['price'],data['store_id']) # '' __init__ method ' of the ItemModel class tells me that I have to put name and price
        item = ItemModel(name, **data) # same thing above
        try:
            item.save_to_db()
        except:
            return {'message': 'an error occurred inserting the item'}, 500
        return item.json(), 201 # 200 means: it's OK ! 201 means: it was creared ! I need the item because is format dict (it seems Json)

    # for production site is recommended put jwt_required() in some http verbs like this one bellow
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item {} deleted'.format(name)}

    # for production site is recommended put jwt_required() in some http verbs like this one bellow
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            # item = ItemModel(name, data['price'],data['store_id']) # or just **data
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        # return {"items": list(map(lambda item: item.json(), items))} # using lambda next(filter(lambda x: x['name'] == name,items), None)
        return {"items": [item.json() for item in items]} # list comprehension
