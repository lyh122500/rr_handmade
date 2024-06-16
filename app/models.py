from . import db

class Category(db.Document):
    name = db.StringField(required=True, unique=True)
    products = db.ListField(db.ReferenceField('Product'))

class Product(db.Document):
    name = db.StringField(required=True)
    attributes = db.StringField(required=True)
    quantity = db.IntField(required=True)
    price = db.FloatField(required=True)
    image_url = db.StringField(required=True)
    seller = db.StringField(required=True)
    category = db.ReferenceField(Category, reverse_delete_rule=db.CASCADE)

class CartItem(db.EmbeddedDocument):
    product = db.ReferenceField(Product)
    quantity = db.IntField(required=True)

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    first_name = db.StringField(required=True)
    password = db.StringField(required=True)

class Cart(db.Document):
    user = db.ReferenceField('User', reverse_delete_rule=db.CASCADE)
    items = db.ListField(db.EmbeddedDocumentField(CartItem))

