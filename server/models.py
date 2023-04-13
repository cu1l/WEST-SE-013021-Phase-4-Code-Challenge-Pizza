from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizza'
    serialize_rules = ('-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurants = db.relationship('RestaurantPizza', backref='pizza')
    restaurantpizzas = association_proxy('restaurants', 'restaurant')

    def __repr__(self):
        return f'<Pizza (id={self.id}, name={self.name}, ingredients={self.ingredients})>'
    
    
    
class RestaurantPizza(db.Model):
    __tablename__ = 'restaurantpizza'
    serialize_rules = ('-pizza.restaurants', '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError('Price must be between the values of 1 and 30')
        return price

    def __repr__(self):
        return f'<RestaurantPizza (id={self.id}, price={self.price})>'
    

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurant'
    serialize_rules = ('-restaurants')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurants = db.relationship('RestaurantPizza', backref='restaurant')
    restaurantpizzas = association_proxy('restaurants', 'pizza')

    def __repr__(self):
        return f'<Restaurant (id={self.id}, name={self.name}, address={self.address})>'