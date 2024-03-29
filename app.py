from flask import Flask, jsonify
import read
import datetime
import json
import requests
from flask import request
import Mosquitopublisher as pub
import testdata
import dbservice as db
#import slydes_demo_server as SDS
import firebaseClient as FBC
ServedURL={}

app = Flask(__name__)
firebaseInstance=FBC.firebase_client()

def reroute(url,payload):
    resp=requests.post(url=url,data=payload)
    print(resp.content)
    return str(resp.content)

@app.route('/')
def index():
    return "This is the official API for South beach's fun team data management. Contact Jagan / Ponmani for any assistance!! "

@app.route('/ga_webhook',methods=['POST'])
def ga_webhook():
    data= json.loads(request.data)
    if(data["queryResult"]['intent']['displayName']=="Turn ON"):
        firebaseInstance.putvalue(child="status",data=1)
        return 'OK'
    elif(data["queryResult"]['intent']['displayName']=="Turn OFF"):        
        firebaseInstance.putvalue(child="status",data=0)
        return 'OK'
    else:
        return 'bad,request',400

@app.route('/getdata')
def getdata():
    return read.getsheetdata()

@app.route('/getsheetdata')
def getsheetdata():
    sheetid=str(request.headers['Sheet-Id'])
    cellrange=str(request.headers['Range'])
    return str(read.getgenericdataarray(sheetid,cellrange=cellrange))

@app.route('/getgooglesheetdata')
def getgooglesheetdata():
    sheetid=str(request.args.get('Sheet-Id'))
    cellrange=str(request.args.get('Range'))
    return jsonify(read.getgenericdataarray(sheetid,cellrange=cellrange))

@app.route('/getdata/users/<slackname>',methods=['GET'])
def getuserdata(slackname):
    data = read.getdataarray()
    for element in data['formatted']:
        if(element['Slack id'].strip().lower() == slackname.strip().lower()):
            return str(element)
    return "No results found!"

@app.route('/forward',methods=['POST'])
def forward():
    print(request)#request.headers.get('forward_target')
    header='https://moviebuffapiai.herokuapp.com/webhook'
    if(request.headers.get('forward_target')):
        header=request.headers.get('forward_target')

    resp=reroute(url=header,payload=str(request.data))
    try:
        pub.Publish(topic='QUBE-AI',message=  'HEADERS:\n' +str(request.headers)+'DATA:\n'+str(request.data))
    except:
        print('publish failed')
    #print request.json
    #print 'headers'
    #print request.headers
    #print 'data'
    #print request.data
    return resp

@app.route('/insertresults',methods=['POST'])
def insertresults():
    result_data=request.data
    print(result_data)
    cur=db.conn.cursor()
    try:
        cur.execute("SELECT insert_results(%s);",(result_data,))
        cur.fetchone()[0]
        db.conn.commit()
    except:
        db.conn.commit()
    try:
        cur.execute("SELECT getkey();")
        resp=cur.fetchone()[0] 
        return str(resp)
    except:
        db.conn.commit()
        return 0

@app.route('/getautomationresults')
def getautomationresults():
    key=str(request.args.get('key'))
    cur=db.conn.cursor()
    data=''
    try:
        cur.execute("select get_results('{0}')".format(key))
        data=cur.fetchone()[0]
    except:
        db.conn.commit()
    return data    




@app.route('/birthdays')
def getbirthdays():
    data=read.getdataarray()
    outdata=[]
    for element in data['formatted']:
        if(parsedate(element['Birth Month'])):
            outdata.append(element)

    return json.dumps(outdata)

@app.route('/results')
def getresults():
    return(testdata.report)    


#
# @app.route('/wish')
# def wish():
#     data=read.getdataarray()
#     outdata=[]
#     for element in data['formatted']:
#         if(parsedate(element['Birth Month'])):
#             outdata.append(element)
#     for item in outdata:
#         URL='https://slack.com/api/chat.postMessage?token=XXXXXXX&channel=%40jaganath&text=Wish you a very happy birthday {USER} :birthday:&pretty=1'
#         URL= URL.replace('{USER}', str(item['Slack id']))
#         requests.post(URL)
#
#     return json.dumps(outdata)

HTML_TEMPLATE="""<html>
<head>
<title>Cheers!!</title>
</head>
<body>
<div style="display:flex;justify-content:center;align-items:center;width:100%;">

 <iframe src="{0}">
    Your browser doesn't support iframes
</iframe>
</div>
	
<meta http-equiv="refresh" content="30">
<body bgcolor="black">
</body>
</html>"""



# @app.route("/greetings")
# def render_greetings():
#     global ServedURL
#     replay=True
#     if(request.args.get('replay')=="false"):
#         replay=False
#     if(replay==True):
#         id=str(request.args.get('id'))
#         url=SDS.get_latest_data(id)
#         return HTML_TEMPLATE.format(url)
#     else:
#         id=str(request.args.get('id'))
#         url=SDS.get_latest_data(id)
#         su=None
#         try:
#             su=ServedURL[id]
#         except:
#             pass
#         if(su!=url):
#             ServedURL[id]=url
#             return HTML_TEMPLATE.format(url) 
#         else:
#             return HTML_TEMPLATE.format("https://data.justickets.co/assets/cheers_tagline.svg")

# def parsedate(indate):
#     month = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
#              'October', 'November', 'December']
#     x = str(datetime.date.today())
#     datearray = x.split('-')
#     indatearray = indate.strip().split(' ')
#     if (indatearray[0].lower() == month[int(datearray[1])].lower() and int(indatearray[1]) == int(datearray[2])):
#         return True
#     else:
#         return False



if __name__ == '__main__':
    from os import environ
    app.run(debug=False , host='0.0.0.0', port=environ.get("PORT", 5000))
