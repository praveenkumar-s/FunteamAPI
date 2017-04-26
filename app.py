from flask import Flask
import read

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/getdata')
def getdata():
    return read.getsheetdata()

@app.route('/getdata/users/<slackname>',methods=['GET'])
def getuserdata(slackname):
    data = read.getdatarray()
    for element in data['formatted']:
        if(element['Slack id'].strip().lower() == slackname.strip().lower()):
            return str(element)
    return "No results found!"


if __name__ == '__main__':
    app.run(debug=False , host='0.0.0.0')