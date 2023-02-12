from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/static')
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
def index():
    
    return "<html><body><a href='file://C:/Users/prog/YandexDisk/LS4/temp/1.pdf' target=_blank>ссылка</a></body></html>" ;


@app.route('/url',methods=["GET"])
def url():
    return jsonify({'url':"temp/1.pdf"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)