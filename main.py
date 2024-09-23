from flask import Flask, jsonify, request, redirect


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def webhook():
    try:
        data = request.get_json(force=False, silent=False, cache=True)
        print(data)
        return 'sucsess'
    except:
        return 'warning' 



if __name__ == '__main__':
    app.run(debug=True)
