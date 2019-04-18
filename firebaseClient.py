import pyrebase
import sys
import os

class firebase_client:
    def __init__(self):        
        config = {
    'apiKey': os.environ['FIREBASE_API_KEY'],
    'authDomain': os.environ['FIREBASE_AUTH_DOMAIN'],
    'databaseURL': os.environ['FIREBASE_DATABASE_URL'],
    'storageBucket': ''
}
        self.firebase = pyrebase.initialize_app(config)
        self.firebase.auth()
    def getdb(self):
        return self.firebase.database()

    def putvalue(self, child, data):
        db= self.firebase.database()
        db.child(child).set(data)
    def getdata(self,tag):
        db= self.firebase.database()
        try:
            return db.child(tag).get().val()
        except:
            return None