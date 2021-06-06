from models.item import ItemModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel
import json

class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('items', 
        required=False,
        action='append'
    )

    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
            if not store:
                return {'message': 'store not found'}, 404
            return store.json()
        except:
            return {'message': 'internal server error'}, 500

    def post(self, name):
        data = Store.parser.parse_args()
        try:
            store = StoreModel.find_by_name(name)
            if store:
                return {'message': "store with the name '{}' already exist".format(name)}
            store = StoreModel(name=name)
            store.save_to_db()

            if data['items']:   
                print("items", data['items'])
                for item_str in data['items']:
                    item = json.loads(item_str.replace("'", "\""))
                    item_model = ItemModel(item['name'], item['price'], store_id=store.id)
                    if not ItemModel.find_by_name(item_model.name):
                        item_model.save_to_db()
            
            return {"message": "store created","store": store.json()}, 201
        except:
            return {'message': 'internal server error'}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name=name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted"}
            

class StoreList(Resource):
    def get(self):
        return {"stores":[x.json() for x in StoreModel.query.all()]}
            