from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["loc-search"]
collection = db["files"]

app = Flask(__name__, static_url_path='/static')
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
@app.route('/search',methods=['GET'])
def index():
    documents = collection.find().limit(10)
    return render_template('index.html', documents=documents)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)