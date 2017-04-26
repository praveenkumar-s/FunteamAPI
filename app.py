from flask import Flask
import read
import datetime
import json
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello,!! World!"

@app.route('/getdata')
def getdata():
    return read.getsheetdata()

@app.route('/getdata/users/<slackname>',methods=['GET'])
def getuserdata(slackname):
    data = read.getdataarray()
    for element in data['formatted']:
        if(element['Slack id'].strip().lower() == slackname.strip().lower()):
            return str(element)
    return "No results found!"

@app.route('/birthdays')
def getbirthdays():
    data=read.getdataarray()
    outdata=[]
    for element in data['formatted']:
        if(parsedate(element['Birth Month'])):
            outdata.append(element)

    return json.dumps(outdata)




def parsedate(indate):
    month = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
             'October', 'November', 'December']
    x = str(datetime.date.today())
    datearray = x.split('-')
    indatearray = indate.strip().split(' ')
    if (indatearray[0] == month[int(datearray[1])] and int(indatearray[1]) == int(datearray[2])):
        return True
    else:
        return False

if __name__ == '__main__':
    from os import environ
    app.run(debug=False , host='0.0.0.0', port=environ.get("PORT", 5000))