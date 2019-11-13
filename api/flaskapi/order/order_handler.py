from flaskapi.order.content_order import ContentOrder
from flaskapi.order.images_order import ImagesOrder
from flaskapi.entities.order_website import OrderWebsiteType

order_type_to_class = {
    'content': ContentOrder,
    'images': ImagesOrder
}


def handle_order(order_website: OrderWebsiteType):
    return order_type_to_class[order_website.order_type] \
        .process(order_website)


def handle_pickup_order(order_website: OrderWebsiteType):
    return order_type_to_class[order_website.order_type] \
        .pickup(order_website.id)
