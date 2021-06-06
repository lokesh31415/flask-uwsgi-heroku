
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):

    # request parser to make sure that we are receiving crt and required fields in the request payload
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
            type=float,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('store_id', 
            type=int,
            required=True,
            help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if not item:
                return {"message": "item not found"}, 404
            return {"item": item.json()}
        except:
            return {"message": "internal server error"}, 500

    
    def post(self, name):
        data = Item.parser.parse_args()
        try:
            if ItemModel.find_by_name(name):
                return {"message": "Item with the name '{}' already exist".format(name)}, 400    
            item = ItemModel(name, data["price"], data['store_id'])
            item.save_to_db()
            return {"item": item.json(), "message": "item created"}, 201 
        except:
            return {"message": "internal server error"}, 500

    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if not item:
                return {"message": "Item not found"}, 400
            item.delete_from_db()
            return {"message": "Item deleted."}
        except:
            return {"message": "internal server error"}, 500

    def put(self, name):
        data = Item.parser.parse_args()
        try:
            item = ItemModel.find_by_name(name)
            if not item:
                item = ItemModel(name, **data)
            else:
                item.price = data['price']
            item.save_to_db()
            return {"item": item.json()}
        except:
            return {"message": "internal server error"}, 500



class ItemList(Resource):
    def get(self):
        return {"items": [x.json() for x in ItemModel.query.all()]}

