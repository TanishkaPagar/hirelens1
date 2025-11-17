# firebase_config.py (optional)
# If you want Firebase auth, install pyrebase4 and paste your firebase keys here.
# Otherwise, do NOT create this file.

import pyrebase

firebaseConfig = {
  "apiKey": "YOUR_API_KEY",
  "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
  "projectId": "YOUR_PROJECT_ID",
  "storageBucket": "YOUR_PROJECT_ID.appspot.com",
  "messagingSenderId": "SENDER_ID",
  "appId": "YOUR_APP_ID",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
