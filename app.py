from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient
import time

client = MongoClient("mongodb://localhost:27017/")
db = client["loc-search"]
collection = db["files"]
collection_log = db["log"]

app = Flask(__name__, static_url_path='/static')

# количество элементов на странице
per_page = 20

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
@app.route('/search',methods=['GET'])
def index():
    query = request.args.get('query',default="")
    
    page = request.args.get('page', type=int, default=1)
    skip = (page - 1) * per_page
    
    db_query = {'file':1,'$text': {'$search': query}}
    db_projection = {'score': {'$meta': 'textScore'}}
    db_sort = [('score', {'$meta': 'textScore'})]
    
    total = collection.count_documents(db_query)
    
    start_time = time.monotonic()
    documents = collection.find(db_query,db_projection).sort(db_sort).skip(skip).limit(per_page)
    end_time = time.monotonic()
    
    elapsed_time = end_time - start_time
    
    document_log = {'date':datetime.now(),'client_ip':request.remote_addr,'query':query, 'page':page, 'total':total, 'elapsed_time':elapsed_time}
    
    collection_log.insert_one(document_log)
    
    return render_template('index.html', documents=documents, query=query, page=page, per_page=per_page, total=total)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)