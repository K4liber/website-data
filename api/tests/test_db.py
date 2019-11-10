import sqlalchemy
import os

from flaskapi.config import config
from flaskapi.entities.order_website import OrderWebsite
from flaskapi.entities.website_content import WebsiteContent
from flaskapi.entities.website_image import WebsiteImage
from flaskapi.entities.base import Base
from flaskapi.run import db_engine

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=db_engine)
session = Session()

def test_order_website_table():
    order_website = OrderWebsite(
        website_url='random.website.url.com',
        order_type='content'
    )
    session.add(order_website)
    session.commit()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(website_url='random.website.url.com').first()
    assert order_website_from_db.website_url == order_website.website_url
    session.delete(order_website_from_db)
    session.commit()
    empty_order = session.query(OrderWebsite) \
        .filter_by(website_url='random.website.url.com').first()
    assert empty_order is None


def test_website_content_table():
    order_website = OrderWebsite(
        website_url='random.website_content.url.com',
        order_type='content'
    )
    session.add(order_website)
    session.commit()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(website_url='random.website_content.url.com').first()
    assert order_website_from_db.website_url == order_website.website_url
    website_content = WebsiteContent(
        content='Example content.',
        order_id=order_website_from_db.id
    )
    session.add(website_content)
    session.commit()
    website_content_from_db = session.query(WebsiteContent) \
        .filter_by(order_id=order_website_from_db.id).first()
    assert website_content.order_id == website_content_from_db.order_website.id
    session.delete(order_website_from_db)
    session.delete(website_content_from_db)
    session.commit()
    empty_order = session.query(WebsiteContent) \
        .filter_by(order_id=order_website_from_db.id).first()
    assert empty_order is None

def test_website_image_table():
    order_website = OrderWebsite(
        website_url='random.website_image.url.com',
        order_type='content'
    )
    session.add(order_website)
    session.commit()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(website_url='random.website_image.url.com').first()
    assert order_website_from_db.website_url == order_website.website_url
    path_to_example_1 = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'example_1.jpg')
    path_to_example_2 = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'example_2.jpg')

    with open(path_to_example_1, 'rb') as example_1_file:
        example_1_img = example_1_file.read()

    with open(path_to_example_2, 'rb') as example_2_file:
        example_2_img = example_2_file.read()

    website_image_1 = WebsiteImage(
        order_id=order_website_from_db.id,
        caption='example_1',
        img=example_1_img
    )
    website_image_2 = WebsiteImage(
        order_id=order_website_from_db.id,
        caption='example_2',
        img=example_2_img
    )
    session.add(website_image_1)
    session.add(website_image_2)
    session.commit()
    website_images_from_db = session.query(WebsiteImage) \
        .filter_by(order_id=order_website_from_db.id).all()

    for website_image_from_db in website_images_from_db:
        assert website_image_1.order_id == website_image_from_db.order_website.id
        session.delete(website_image_from_db)

    session.delete(order_website_from_db)
    session.commit()
    empty_order = session.query(WebsiteImage) \
        .filter_by(order_id=order_website_from_db.id).first()
    assert empty_order is None
