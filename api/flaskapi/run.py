from flaskapi.app import create_app
from flaskapi.entities.base import Base
from flaskapi.entities.order_website import OrderWebsite
from flaskapi.entities.website_content import WebsiteContent
from flaskapi.entities.website_image import WebsiteImage
from flaskapi.config import config
from sqlalchemy import create_engine

api = create_app(__name__)
db_engine = create_engine(
    f'mysql+mysqlconnector://{config["db"]["user"]}:{config["db"]["password"]}' \
    f'@{config["db"]["host"]}:{config["db"]["port"]}/{config["db"]["database"]}')

@api.route("/")
def print_status():
    return 'website-data is working.'

if __name__ == '__main__':
    Base.metadata.create_all(db_engine)
    api.run(debug=False, host='0.0.0.0')
