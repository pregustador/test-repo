from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self,username,password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username): # I can put self as argument to reference User in this function, but I prefer user @classmethod and put cls to referene class
        return cls.query.filter_by(username=username).first() # sql: "SELECT * FROM users WHERE username=usernaname LIMIT 1"

    @classmethod
    def find_by_id(cls,_id): # I can put self as argument to reference User in this function, but I prefer user @classmethod and put cls to referene class
        return cls.query.filter_by(id=_id).first() # sql: "SELECT * FROM users WHERE username=usernaname LIMIT 1"

    def save_to_db(self): # SQLAlchemy substitute insert and update automatic
        db.session.add(self) # sql: "INSERT INTO items VALUES (...)"
        db.session.commit()
