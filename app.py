from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os
#from flask_session import Session

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
migrate = Migrate(app, db)


class cpu(db.Model):
    cpu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpu_rank = db.Column(db.Integer)
    cpu_model = db.Column(db.String(150))


def __init__(self, cpu_id, cpu_rank, cpu_model):
    self.cpu_id = cpu_id
    self.cpu_rank = cpu_rank
    self.cpu_model = cpu_model


class cpuSchema(ma.Schema):
    class Meta:
        fields = ('cpu_id', 'cpu_rank', 'cpu_model')


cpu_schema = cpuSchema()
cpu_schema = cpuSchema(many=True)


# Product Class/Model
class Product(db.Model):
    mobile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ram = db.Column(db.Integer)
    storage_size = db.Column(db.Integer)
    cpu_id = db.Column(db.Integer, db.ForeignKey('cpu.cpu_id'))
    ppi = db.Column(db.Integer)
    price_egp = db.Column(db.Integer)
    rank_selfie = db.Column(db.Integer)
    rank_weights_selfie = db.Column(db.Integer)
    rank_maincamera = db.Column(db.Integer)
    rank_weights_main_camera = db.Column(db.Integer)
    battery_endurance_time = db.Column(db.Integer)
    display_protection = db.Column(db.Integer)
    mobile = db.Column(db.String(70))
    rank_weights_models = db.Column(db.Integer)

    def __init__(self, ram, cpu_id, storage_size,
                 ppi, price_egp,
                 rank_selfie, rank_weights_selfie, rank_maincamera,
                 rank_weights_mani_camera, battery_endurance_time, display_protection, mobile,rank_weights_models):
        self.ram = ram
        self.storage_size = storage_size
        self.cpu_id = cpu_id
        self.ppi = ppi
        self.price_egp = price_egp
        self.rank_selfie = rank_selfie
        self.rank_weights_selfie = rank_weights_selfie
        self.rank_maincamera = rank_maincamera
        self.rank_weights_mani_camera = rank_weights_mani_camera
        self.battery_endurance_time = battery_endurance_time
        self.display_protection = display_protection
        self.mobile = mobile
        self.rank_weights_models=rank_weights_models


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('mobile_id ', 'ram', 'cpu_id', 'storage_size', 'ppi', 'price_egp',
                  'rank_selfie', 'rank_weights_selfie', 'rank_maincamera', 'rank_weights_main_camera',
                  'battery_endurance_time', 'display_protection', 'mobile','rank_weights_models')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class AffiliationBusiness(db.Model):
    aff_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    aff_name = db.Column(db.String(70))
    website_link = db.Column(db.String(500))

    def __init__(self, aff_id, aff_name, website_link):
        self.aff_id = aff_id
        self.aff_name = aff_name
        self.website_like = website_link
class AffiliationBusinessSchema(ma.Schema):
    class Meta:
        fields = ('aff_id','aff_name','website_link')

AffiliationBusiness_schema = AffiliationBusinessSchema()
AffiliationBusiness_schema = AffiliationBusinessSchema(many=True)



class AffiliationSelectedMobile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    mobile_id = db.Column(db.Integer, db.ForeignKey(Product.mobile_id))
    aff_id = db.Column(db.Integer, db.ForeignKey(AffiliationBusiness.aff_id))
    date_of_choice = db.Column(db.DateTime)

    def __init__(self, mobile_id, aff_id, date_of_choice):
        self.mobile_id = mobile_id
        self.aff_id = aff_id
        self.date_of_choice = date_of_choice

class AffiliationSelectedMobileSchema(ma.Schema):
    class Meta:
        fields = ('mobile_id','aff_id','date_of_choice')
AffiliationSelectedMobile_schema = AffiliationSelectedMobileSchema()
AffiliationSelectedMobile_schema = AffiliationSelectedMobileSchema(many=True)

# ennnd modelllllllls __________________________________________________

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
    ram = request.json['ram']
    storage_size = request.json['storage_size']
    cpu_id = request.json['cpu_id']
    ppi = request.json['ppi']
    price_egp = request.json['price_egp']
    rank_selfie = request.json['rank_selfie']
    rank_weights_selfie = request.json['rank_weights_selfie']
    rank_maincamera = request.json['rank_maincamera']
    rank_weights_main_camera = request.json['rank_weights_main_camera']
    battery_endurance_time = request.json['battery_endurance_time']
    display_protection = request.json['display_protection']
    mobile = request.json['mobile']
    rank_weights_models=request.json['rank_weights_models']
    new_product = Product(ram, storage_size, cpu_id, ppi, price_egp, rank_selfie, rank_weights_selfie,
                          rank_maincamera, rank_weights_main_camera, battery_endurance_time, display_protection, mobile,rank_weights_models)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update a Product
@app.route('/product/<mobile_id>', methods=['PUT'])
def update_product(mobile_id):
    product = Product.query.get(mobile_id)

    ram = request.json['ram']
    storage_size = request.json['storage_size']
    cpu_id = request.json['cpu_id']
    ppi = request.json['ppi']
    price_egp = request.json['price_egp']
    rank_selfie = request.json['rank_selfie']
    rank_weights_selfie = request.json['rank_weights_selfie']
    rank_maincamera = request.json['rank_maincamera']
    rank_weights_main_camera = request.json['rank_weights_main_camera']
    battery_endurance_time = request.json['battery_endurance_time']
    display_protection = request.json['display_protection']
    mobile = request.json['mobile']
    rank_weights_models = request.json['rank_weights_models']
    product.ram = ram
    product.storage_size = storage_size
    product.cpu_id = cpu_id
    product.price_egp = price_egp
    product.rank_selfie = rank_selfie
    product.rank_weights_selfie = rank_weights_selfie
    product.rank_maincamera = rank_maincamera
    product.rank_weights_main_camera = rank_weights_main_camera
    product.battery_endurance_time = battery_endurance_time
    product.display_protection = display_protection
    product.mobile = mobile
    product.rank_weights_models=rank_weights_models
    db.session.commit()

    return product_schema.jsonify(product)


# Delete Product
@app.route('/product/<mobile_id>', methods=['DELETE'])
def delete_product(mobile_id):
    product = Product.query.get(mobile_id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)
# Query on the DataBase

@app.route('/top10Battery', methods=['GET'])
def top10Battery():
    topbattery= Product.query.order_by(Product.battery_endurance_time.desc()).limit(10).all()
    result = products_schema.dump(topbattery)
    return jsonify(result)


@app.route('/top10Camera', methods=['GET'])
def top10Camera():
    topcamera= Product.query.order_by(Product.rank_weights_main_camera).limit(10).all()
    result = products_schema.dump(topcamera)
    return jsonify(result)


@app.route('/top10Screen', methods=['GET'])
def top10Screen():
    topscreen= Product.query.order_by(Product.ppi.desc()).limit(10).all()
    result = products_schema.dump(topscreen)
    return jsonify(result)


@app.route('/top10cpu', methods=['GET'])
def top10cpu():
    #topcpu= cpu.query.
    #result=cpu_schema.dump(topcpu)
    #topcpu = db.session.query(cpu, Product).join(Product).filter(cpu.cpu_id == Product.cpu_id).order_by(cpu.cpu_rank).limit(10).all()
    topcpu = Product.query.join(cpu,cpu.cpu_id == Product.cpu_id).order_by(cpu.cpu_rank).limit(10).all()
    result = products_schema.dump(topcpu)
    return jsonify(result)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
