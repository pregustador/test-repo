from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # the items have may items
    items = db.relationship('ItemModel', lazy='dynamic') # allow us to do the relationship with the class ItemModel and this relation is store_id that we referenced in class 'StoreModel'
    # obs.: lazy = 'dynamic means we tell tell the sqlalchemy that do not to look ItemModel make a object of each item, because has a exepensive operation cost for many items
    # obs.: now 'items' is not a list of item, because we put lazy='dynamic'

    def __init__(self,name):
        self.name = name

    # here we prefere the speed creation store instaed speed call jason() method, becasue every time that json() is called it has to look into items table
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} # In this case, because od lazy='dynamic', self.items is query builder that has a property to look into items table. Becasue of that we need all() at the end


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
