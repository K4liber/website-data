from rq import Worker, Connection, Queue

from flaskapi.entities.order_website import OrderWebsite
from flaskapi.order.order_handler import (
    handle_order,
    handle_pickup_order
)
from flaskapi.init import (
    Session,
    redis_queue,
    redis_conn,
    listen
)


def order_status(order_id: int):
    session = Session()
    order_website = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()

    if order_website is None:
        status = 'Unknown'
    elif order_website.order_status:
        status = 'Finished'
    else:
        status = 'Unfinished'

    session.close()
    return status


def order_website(website_url: str, order_type: str):
    session = Session()
    order_website = OrderWebsite(
        website_url=website_url,
        order_type=order_type
    )
    session.add(order_website)
    session.commit()
    session.refresh(order_website)
    session.close()
    job = redis_queue.enqueue_call(
        func=handle_order, args=(order_website,), job_id=str(order_website.id)
    )
    return job.get_id()


def pickup_order(order_id: int):
    session = Session()
    order_website = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()
    session.close()

    if order_website is None:
        result = f'Order unknown with ID = {order_id}'
    elif order_website.order_status:
        order_data = handle_pickup_order(order_website)
        result = order_data
    else:
        result = f'Order with ID = {order_id} is not ready.' \
            f'Wait for it or try again.'

    return result


if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
