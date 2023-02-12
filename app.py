from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/static')
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
def index():
    return "<html><body><iframe src='http://C:/Users/prog/YandexDisk/LS4/file.html'>iframe не работает</iframe></body></html>" ;



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)