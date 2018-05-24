from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test",methods=['GET'])
def test():
    return "test"



def main():
    app.run(host='0.0.0.0', port=80)
    # app.run()


if __name__ == '__main__':
    main()