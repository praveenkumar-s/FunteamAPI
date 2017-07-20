
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_credentials_srvc():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scopes=SCOPES)
    return credentials


def getsheetdata():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials_srvc()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1-k4_LLWE1KfNWksNt0OkFIxpDSy-Xu2md84PC7zMzuw'
    rangeName = '2017-2018!A1:Z62'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        #print('Name, Major:')
        #for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
        #    print('%s, %s' % (row[0], row[1]))
        mdict=[]
        for j in range(1, len(values)):
            dict = {}
            for i in range(0, len(values[0])):
                val=''
                try:
                    val = str(values[j][i])
                except:
                    val=''
                dict[values[0][i]] = val
            mdict.append(dict)
        data = {}
        data['key'] = 'value'
        json_data = json.dumps(mdict)
        return json_data

def getdataarray():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials_srvc()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1-k4_LLWE1KfNWksNt0OkFIxpDSy-Xu2md84PC7zMzuw'
    rangeName = '2017-2018!A1:Z62'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        #print('Name, Major:')
        #for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
        #    print('%s, %s' % (row[0], row[1]))
        mdict=[]
        for j in range(1, len(values)):
            dict = {}
            for i in range(0, len(values[0])):
                val=''
                try:
                    val = str(values[j][i])
                except:
                    val=''
                if(values[0][i]!=''):
                    dict[values[0][i]] = val
            mdict.append(dict)
        obj={}
        obj['rawdata']=values
        obj['formatted']=mdict
        return obj



#x=getdatarray()

#for e in x['formatted']:
#    print (e['Slack id'])
