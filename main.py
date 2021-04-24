from business import Business
from authorization import Authorization
import pymongo
from app import create_app
from persistence_gateway import UserRepository, TemplateRepository
import os

SpiceBlue_connection_string = os.environ.get('SpiceBlue_connection_string')
SpiceBlue_connection_string = "mongodb+srv://test:test@cluster0.z8mo0.mongodb.net/mydatabase?retryWrites=true&w=majority"
mongo_client = pymongo.MongoClient(SpiceBlue_connection_string)
templates_db = mongo_client["mydatabase"]
SpiceBlue_authorization_secret = os.environ.get('SpiceBlue_authorization_secret')
authorization = Authorization(SpiceBlue_authorization_secret)
template_repository = TemplateRepository(templates_db)
user_repository = UserRepository(templates_db)
template_service = Business(template_repository, authorization, user_repository)
app = create_app(template_service)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
