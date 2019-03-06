from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # if from table stores
    store = db.relationship('StoreModel') # allow us to do the relationship with the class StoreModel and this relation is store_id that we referenced in line above

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # sql: "SELECT * FROM items WHERE name=name LIMIT 1"
        # obs.: # I can put other filter after the first filter or filter multiple filter_by(something=some,someone= any) ...
        # obs.: I can use ItemModel instead cls

    def save_to_db(self): # SQLAlchemy substitute insert and update automatic
        db.session.add(self) # sql: "INSERT INTO items VALUES (...)"
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self) # sql: "DELETE FROM items WHERE name=..."
        db.session.commit()
