from bs4 import BeautifulSoup
import requests
import re
import zipfile
from flask import Response
import os
from requests.exceptions import MissingSchema

from flaskapi.order.order import Order
from flaskapi.entities.order_website import (
    OrderWebsite,
    OrderWebsiteType
)
from flaskapi.entities.website_image import WebsiteImage
from flaskapi.init import Session

supported_img_types = {
    'image/gif': 'gif',
    'image/jpeg': 'jpeg',
    'image/jpg': 'jpg',
    'image/png': 'png'
}


class ImagesOrder(Order):
    @classmethod
    def process(self, order_website: OrderWebsiteType):
        session = Session()
        order_website_from_db = session.query(OrderWebsite) \
            .filter_by(id=order_website.id).first()

        if order_website_from_db is not None:
            request = requests.get(order_website.website_url)
            soup = BeautifulSoup(request.text, 'html.parser')
            images = soup.findAll('img', {'alt': True, 'src': True})

            for img in images:
                img_url = img['src']

                try:
                    response = requests.get(img_url)
                except MissingSchema:
                    img_url = order_website_from_db.website_url + \
                        '/' + img['src']
                try:
                    response = requests.get(img_url)
                except MissingSchema:
                    print(f'Wrong image address: "{img_url} for website "'
                          f'"{order_website_from_db.website_url}".')
                    continue

                img_data = response.content
                img_type = response.headers['content-type']

                if img_type not in supported_img_types:
                    continue

                if img['alt']:
                    img_alt = str(
                        re.sub(r'\W+', ' ', img['alt']).encode('utf-8'))
                else:
                    img_alt = ''

                website_image = WebsiteImage(
                    order_id=order_website.id,
                    caption=img_alt,
                    img=img_data,
                    img_type=img_type
                )
                session.add(website_image)
                session.commit()

            order_website_from_db.order_status = True
            session.commit()
            session.close()

    @classmethod
    def pickup(self, order_id: int):
        session = Session()
        website_images_from_db = session.query(WebsiteImage) \
            .filter_by(order_id=order_id).all()

        if len(website_images_from_db) == 0:
            return f'There are no images for order with ID = {order_id}'

        zf_filename = f'order_{order_id}.zip'
        zf_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../../..', zf_filename
        )
        zf = zipfile.ZipFile(zf_path, mode='w')

        for website_image in website_images_from_db:
            img_ext = supported_img_types[website_image.img_type]
            img_filename = f'img_{website_image.id}.{img_ext}'
            img_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '../../..', img_filename
            )
            f = open(img_path, 'wb')
            f.write(website_image.img)
            f.close()
            zf.write(img_path)
            os.remove(img_path)

        zf.close()

        with open(zf_path, 'rb') as response_zip_file:
            response = response_zip_file.read()

        os.remove(zf_path)
        return Response(response)
