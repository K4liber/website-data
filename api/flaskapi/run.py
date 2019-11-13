from flask import request
from sqlalchemy.exc import InterfaceError

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


@api.route("/")
def print_status():
    return 'website-data is working...'


@api.route("/order_website", methods=['POST'])
def order_website_route():
    request_data = request.get_json()
    website_url = request_data['website_url']
    order_type = request_data['order_type']

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

    db_connection.close()
    print('Connection to db established.')
    Base.metadata.create_all(db_engine)
    api.run(debug=False, host='0.0.0.0')
