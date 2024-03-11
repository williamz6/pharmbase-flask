from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from pharmbase import db, login_manager
from pharmbase import db, login_manager
from datetime import datetime, date

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))
# Define User data-model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # User fields
    
    first_name = db.Column(db.String(50), autoincrement=True, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False,  unique=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email_confirmed_at = db.Column(db.DateTime())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  
    

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', {self.email})"
       
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    
    def is_active(self):
        """Always True, as all users are active."""
        return True

    
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)
    


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    users = db.relationship('User', backref='role',
                                lazy='dynamic')
 
    def __init__(self, name):

        self.name = name
class Drug(db.Model, UserMixin):
    
    __tablename__= "drugs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False,  unique=True)
    description= db.Column(db.Text, nullable= False)
    date_added= db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    quantity_received= db.Column(db.Integer, nullable=False)
    available_quantity= db.Column(db.Integer, nullable=False)
    expiry_date= db.Column(db.DateTime) 
    orders= db.relationship('Order', backref='drugs', lazy=True)

    def __init__(self, name, description, date_added, quantity_received, available_quantity, expiry_date):
        self.name= name
        self.description= description
        self.date_added= date_added
        self.quantity_received= quantity_received
        self.available_quantity= available_quantity
        self.expiry_date= expiry_date

    def __repr__(self):
        return f"Drug('{self.name}', '{self.date_added}', '{self.quantity_received}', '{self.available_quantity}', '{self.expiry_date}')"
 

class Order(db.Model):
    __tablename__= "orders"
    id= db.Column(db.Integer, primary_key=True)
    drug_id= db.Column(db.Integer, db.ForeignKey('drugs.id'))
    quantity_received= db.Column(db.Integer, nullable=False)
    location= db.Column(db.String(100), nullable=False)
    time_shipped= db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)
    def __init__(self, drug_id, quantity_received, location, time_shipped):
        self.drug_id = drug_id
        self.quantity_received = quantity_received
        self.location = location
        self.time_shipped = time_shipped
    