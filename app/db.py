
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import getenv

#db_password = "mROWJyCNfAshZUyl"

db_password = getenv('MONGODB_PASS')

#print(f'db pass: {db_password}')

#uri = f'mongodb+srv://alkimdogan06:mROWJyCNfAshZUyl@cluster0.xvymk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
uri = f'mongodb+srv://alkimdogan06:{db_password}@cluster0.xvymk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

def get_db():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api = ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client['flask_db']
    except Exception as e:
        print(e)
