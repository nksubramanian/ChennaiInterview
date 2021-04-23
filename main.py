from business import Business
from authorization import Authorization
import pymongo
from app import create_app
from persistence_gateway import UserRepository, TemplateRepository

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
templates_db = mongo_client["mydatabase"]
authorization = Authorization()
template_repository = TemplateRepository(templates_db)
user_repository = UserRepository(templates_db)
template_service = Business(template_repository, authorization, user_repository)
app = create_app(template_service)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
