from flask import Flask
import read
import datetime
import json
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return "This is the official API for South beach's fun team data management. Contact Jagan / Ponmani for any assistance!! "

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


@app.route('/wish')
def wish():
    data=read.getdataarray()
    outdata=[]
    for element in data['formatted']:
        if(parsedate(element['Birth Month'])):
            outdata.append(element)
    for item in outdata:
        URL='https://slack.com/api/chat.postMessage?token=xoxp-2517532264-126093546167-175381339458-da20ef65b49197d76c8dd49c5ec3813b&channel=%40jaganath&text=Wish you a very happy birthday {USER} :birthday:&pretty=1'
        URL= URL.replace('{USER}', str(item['Slack id']))
        requests.post(URL)

    return json.dumps(outdata)




def parsedate(indate):
    month = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
             'October', 'November', 'December']
    x = str(datetime.date.today())
    datearray = x.split('-')
    indatearray = indate.strip().split(' ')
    if (indatearray[0].lower() == month[int(datearray[1])].lower() and int(indatearray[1]) == int(datearray[2])):
        return True
    else:
        return False

if __name__ == '__main__':
    from os import environ
    app.run(debug=False , host='0.0.0.0', port=environ.get("PORT", 5000))