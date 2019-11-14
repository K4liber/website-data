from flask import request
from sqlalchemy.exc import InterfaceError, ProgrammingError
from sqlalchemy import create_engine
from urllib.parse import urlparse

from flaskapi.entities.base import Base
from flaskapi.init import (
    api,
    db_engine
)
from flaskapi.worker import (
    order_website,
    order_status,
    pickup_order
)
from flaskapi.order.order_handler import order_type_to_class
from flaskapi.config import config


@api.route("/")
def print_status():
    return 'website-data is working...'


@api.route("/order_website", methods=['POST'])
def order_website_route():
    request_data = request.get_json()
    website_url = request_data['website_url']
    order_type = request_data['order_type']
    parse_result = urlparse(website_url)

    if not all([parse_result.scheme, parse_result.netloc]):
        return f'`{website_url}` url have a wrong pattern.\n' \
            f'URL correct patters: `http://name.domain(/optional_parts)`.\n'

    if order_type in order_type_to_class:
        order_id = order_website(website_url, order_type)
        return f'Your order ID: {order_id}\n'
    else:
        return f'Incorrect order type `{order_type}`.\n' \
            f'Available order types: {set(order_type_to_class.keys())}\n'


@api.route("/order_status/<order_id>", methods=['GET'])
def order_status_route(order_id: str):
    try:
        order_id = int(order_id)
    except ValueError:
        return 'Order ID should be an integer type.\n'

    status = order_status(order_id)
    return f'Order (ID: {order_id}) status: {status}.\n'


@api.route("/pickup_order/<order_id>", methods=['GET'])
def pickup_order_route(order_id: str):
    try:
        order_id = int(order_id)
    except ValueError:
        return 'Order ID should be an integer type.'

    return pickup_order(order_id)


if __name__ == '__main__':
    db_connection = None
    print('Connecting to db ...')

    while db_connection is None:
        try:
            db_connection = db_engine.connect()
        except InterfaceError:
            db_connection = None
        except ProgrammingError:
            tmp_engine = create_engine(
                f'mysql+mysqlconnector://'
                f'{config["db"]["user"]}:{config["db"]["password"]}'
                f'@{config["db"]["host"]}:{config["db"]["port"]}')
            db_list = [d[0] for d in tmp_engine.execute("SHOW DATABASES;")]
            db_name = config['db']['name']

            if db_name not in db_list:
                tmp_engine.execute(f'CREATE DATABASE {db_name}')
                print(f'Created database {db_name}')

    db_connection.close()
    print('Connection to db established.')
    Base.metadata.create_all(db_engine)
    api.run(debug=False, host='0.0.0.0')
