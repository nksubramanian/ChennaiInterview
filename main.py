from business import Business
from authorization import Authorization
import pymongo
from app import create_app
from persistence_gateway import UserRepository, TemplateRepository
import os

connection_string = os.environ.get('connection_string')
mongo_client = pymongo.MongoClient(connection_string)
templates_db = mongo_client["mydatabase"]
key = os.environ.get('key')
authorization = Authorization("secret1")
template_repository = TemplateRepository(templates_db)
user_repository = UserRepository(templates_db)
template_service = Business(template_repository, authorization, user_repository)
app = create_app(template_service)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
