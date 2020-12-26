import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = 'capstone'
    database_path = 'postgresql://jaimeaznar@{}/{}'.format('localhost:5432',database_name)

db = SQLAlchemy()


def setup_db(app):
    app.config.from_object('config.DevelopmentConfig')
    db.app = app
    db.init_app(app)
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # relationship with product
    product = db.relationship(
        "Product", back_populates="company",
        cascade="all, delete,delete-orphan",
        passive_deletes=True
    )

    def __init__(self, name, city, state, address, phone):
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    



class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image_link = db.Column(db.String(500))
    product_description = db.Column(db.Text)
    #relationship
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))

    company = db.relationship("Company", back_populates="product")


    def __init__(self, name, image_link, product_description):
        self.name = name
        self.image_link = image_link
        self.product_description = product_description
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

