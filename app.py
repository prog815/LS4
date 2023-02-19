from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from bson import json_util

client = MongoClient("mongodb://localhost:27017/")
db = client["loc-search"]
collection = db["files"]

app = Flask(__name__, static_url_path='/static')
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
def index():
    return "hi" ;

@app.route('/get',methods=['GET'])
def get_data():
    data = {'name': 'John', 'age': 30}
    return jsonify(data)

@app.route('/search',methods=['GET'])
def search():
    # query = request.args.get('query')
    
    page_size = 10
    page_number = request.args.get('page_number')
    
    try:
        page_number = int(page_number)
    except:
        page_number = 1
        
    documents_to_skip = page_size * (page_number - 1)
    
    documents = collection.find().skip(documents_to_skip).limit(page_size)
    
    return jsonify(json_util.dumps(documents))
    
 
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)