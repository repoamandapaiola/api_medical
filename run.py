from pymongo import MongoClient

from app.app import create_app
client = MongoClient(host='localhost')
app = create_app(session_database=client)

app.run('0.0.0.0', port=9090)