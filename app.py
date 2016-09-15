from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
e = create_engine('sqlite:///address.db')
app = Flask(__name__)
api = Api(app)
class Address_Meta(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from address")
        return {'data': [i[0] for i in query.cursor.fetchall()]}
class Address_Suburb(Resource):
    def get(self, suburb_name):
        conn = e.connect()
        query = conn.execute("select * from address where Suburb='%s'"%suburb_name.upper())
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class Address_Geocode(Resource):
    def get(self, postal_code):
        conn = e.connect()
        query = conn.execute("select Longitude, Latitude from address where Postcode='%d'"%postal_code)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

api.add_resource(Address_Suburb, '/api/v1.0/suburb/<string:suburb_name>')
api.add_resource(Address_Meta, '/api/v1.0/address')
api.add_resource(Address_Geocode, '/api/v1.0/geocode/<int:postal_code>')
if __name__ == '__main__':
     app.run(host="0.0.0.0",port=5010)
