from business import Business
from authorization import Authorization
import pymongo
from app import create_app
from persistence_gateway import UserRepository, TemplateRepository
import os


def __get_env_variable(env_variable_name, default_value):
    env_variables = os.environ
    env_variable_value = default_value
    if env_variable_name in env_variables.keys():
        env_variable_value = env_variables[env_variable_name]
    return env_variable_value


secret = __get_env_variable('SPICEBLUE_AUTHORIZATION_SECRET', "secret")
authorization = Authorization(secret)


default_uri = "mongodb+srv://test:test@cluster0.z8mo0.mongodb.net/mydatabase?retryWrites=true&w=majority"
database_uri = __get_env_variable("SPICEBLUE_CONNECTION_STRING", default_uri)
mongo_client = pymongo.MongoClient(database_uri)
templates_db = mongo_client["mydatabase"]
template_repository = TemplateRepository(templates_db)
user_repository = UserRepository(templates_db)

template_service = Business(template_repository, authorization, user_repository)
app = create_app(template_service)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

