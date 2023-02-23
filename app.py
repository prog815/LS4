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
    query = request.args.get('query')
    
    db_query = {'file':1,'$text': {'$search': query}}
    db_projection = {'score': {'$meta': 'textScore'}}
    db_sort = [('score', {'$meta': 'textScore'})]
    
    documents = collection.find(db_query,db_projection).sort(db_sort).limit(20)
    
    return render_template('index.html', documents=documents,query=query)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)