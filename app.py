from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
def index():
    return "привет с сервера"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)