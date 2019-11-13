from abc import ABC, abstractclassmethod

from flaskapi.entities.order_website import OrderWebsiteType


class Order(ABC):
    @abstractclassmethod
    def process(self, order_website: OrderWebsiteType):
        pass

    @abstractclassmethod
    def pickup(self, order_id: int):
        pass
