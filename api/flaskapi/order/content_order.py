import requests
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import json

from flaskapi.order.order import Order
from flaskapi.entities.website_content import WebsiteContent
from flaskapi.init import Session
from flaskapi.entities.order_website import OrderWebsiteType


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head',
                               'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


class ContentOrder(Order):
    @classmethod
    def process(self, order_website: OrderWebsiteType):
        session = Session()
        request = requests.get(order_website.website_url)
        soup = BeautifulSoup(request.text, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        content = u' '.join(t.strip() for t in visible_texts)
        clean_content = re.sub(r'\W+', ' ', content).encode('utf-8')
        website_content = WebsiteContent(
            order_id=order_website.id,
            content=str(clean_content)
        )
        session.add(website_content)
        session.commit()
        website_content.order_website.order_status = True
        session.commit()
        session.close()

    @classmethod
    def pickup(self, order_id: int):
        session = Session()
        website_content_from_db = session.query(WebsiteContent) \
            .filter_by(order_id=order_id).first()

        if website_content_from_db is None:
            return f'Empty content for order with ID = {order_id}'

        return json.dumps(website_content_from_db.to_dict())
