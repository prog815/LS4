from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient
import time
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["loc-search"]
collection = db["files"]
collection_log = db["log"]

app = Flask(__name__, static_url_path='/static')

# количество элементов на странице
per_page = 20

source = os.environ.get('SOURCE')  

@app.template_filter('get_dir')
def get_dir_from_path(rel_path):
    
    path_to_base_dir = "./static/files"
    
    
    file_path = os.path.join(path_to_base_dir , rel_path )
    dir_path = os.path.dirname(file_path)
    
    path_to_target_dir = dir_path
    
    relative_path = os.path.relpath(path_to_target_dir, path_to_base_dir)
    
    return os.path.join(source,relative_path)

@app.template_filter('filesize')
def format_filesize(value):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while value >= 1024 and index < len(units) - 1:
        value /= 1024
        index += 1
    return '{:.1f} {}'.format(value, units[index])


@app.template_filter('enumerate')
def enumerate_filter(seq, start=0):
    return enumerate(seq, start=start)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)

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
    
    document_log = {'date':datetime.now(),
                    'client_ip':request.remote_addr,
                    'query':query, 
                    'page':page, 
                    'total':total, 
                    'elapsed_time':elapsed_time}
    
    collection_log.insert_one(document_log)
    
    return render_template('index.html', 
                           documents=documents, 
                           query=query, 
                           page=page, 
                           per_page=per_page, 
                           total=total, 
                           source=source)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)