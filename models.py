import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def setup_db(app, database_path):
    app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    db.app = app
    db.init_app(app)
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
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
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # relationship
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'company.id',
            ondelete='CASCADE'))

    company = db.relationship("Company", back_populates="product")

    def __init__(self, name, image, description, company_id):
        self.name = name
        self.image = image
        self.description = description
        self.company_id = company_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
