import requests
import time
import json
import zipfile
import os

from tests.test_db import Session
from flaskapi.entities.order_website import OrderWebsite
from flaskapi.entities.website_content import WebsiteContent
from flaskapi.entities.website_image import WebsiteImage
from flaskapi.order.images_order import supported_img_types


def test_order_wrong_type():
    url = 'http://api:5000/order_website'
    incorrect_order_type = "headers"
    data = {
        "website_url": "http://90minut.pl",
        "order_type": incorrect_order_type
    }
    r = requests.post(url, verify=False, json=data)
    print(r.text)
    assert r.text.split('\n')[0] == \
        f'Incorrect order type `{incorrect_order_type}`.'


def test_order_website_content():
    url = 'http://api:5000/order_website'
    data = {
        "website_url": "http://90minut.pl",
        "order_type": "content"
    }
    r = requests.post(url, verify=False, json=data)
    assert r.status_code == 200
    order_id = r.text.split()[-1]
    session = Session()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()
    assert order_website_from_db.website_url == "http://90minut.pl"

    if order_website_from_db.order_status:
        website_content_from_db = session.query(WebsiteContent) \
            .filter_by(order_id=order_id).first()
        assert website_content_from_db is not None
        session.delete(website_content_from_db)
    else:
        website_content_from_db = session.query(WebsiteContent) \
            .filter_by(order_id=order_id).first()
        assert website_content_from_db is None

    session.delete(order_website_from_db)
    session.commit()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()
    session.close()
    assert order_website_from_db is None


def test_order_website_images():
    url = 'http://api:5000/order_website'
    data = {
        "website_url": "http://facebook.pl",
        "order_type": "images"
    }
    r = requests.post(url, verify=False, json=data)
    assert r.status_code == 200
    order_id = r.text.split()[-1]
    session = Session()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()
    start_time = time.time()

    while order_website_from_db is None:
        if time.time() - start_time > 10:
            break
        order_website_from_db = session.query(OrderWebsite) \
            .filter_by(id=order_id).first()

    assert time.time() - start_time < 10
    session.close()
    assert order_website_from_db.website_url == "http://facebook.pl"

    if order_website_from_db.order_status:
        session = Session()
        website_images_from_db = session.query(WebsiteImage) \
            .filter_by(order_id=order_id).all()
        assert website_images_from_db is not None

        for website_image in website_images_from_db:
            assert website_image.order_id == order_website_from_db.id
            session.delete(website_image)

    website_images_from_db = session.query(WebsiteImage) \
        .filter_by(order_id=order_id).first()
    assert website_images_from_db is None
    session.delete(order_website_from_db)
    session.commit()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()
    session.close()
    assert order_website_from_db is None


def test_order_status():
    session = Session()
    url = 'http://api:5000/order_status/9999999999'
    r = requests.get(url)
    assert r.status_code == 200
    order_status_message = r.text.split()[-1]
    assert order_status_message == 'Unknown.'
    order_website = OrderWebsite(
        website_url='http://test_order_status_url.pl',
        order_type='content',
        order_status=True,
    )
    session.add(order_website)
    session.commit()
    url = f'http://api:5000/order_status/{order_website.id}'
    r = requests.get(url)
    assert r.status_code == 200
    order_status_message = r.text.split()[-1]
    assert order_status_message == 'Finished.'
    session.delete(order_website)
    session.commit()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(id=order_website.id).first()
    assert order_website_from_db is None
    session.close()


def test_pickup_order_content():
    url = 'http://api:5000/order_website'
    data = {
        "website_url": "http://facebook.pl",
        "order_type": "content"
    }
    r = requests.post(url, verify=False, json=data)
    assert r.status_code == 200
    order_id = r.text.split()[-1]
    session = Session()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()
    start_time = time.time()

    while order_website_from_db.order_status == False:
        if time.time() - start_time > 10:
            break
        session.commit()

    assert time.time() - start_time < 10
    website_content_from_db = session.query(WebsiteContent) \
        .filter_by(order_id=order_id).first()
    assert website_content_from_db is not None
    assert order_website_from_db.order_status
    url = f'http://api:5000/pickup_order/{order_id}'
    r = requests.get(url)
    response_dict = json.loads(r.content.decode('utf-8'))

    for key in response_dict.keys():
        assert key in {'order_id', 'content'}
    
    session.delete(order_website_from_db)
    session.delete(website_content_from_db)
    session.commit()
    session.close()


def test_pickup_order_images():
    url = 'http://api:5000/order_website'
    data = {
        "website_url": "http://facebook.pl",
        "order_type": "images"
    }
    r = requests.post(url, verify=False, json=data)
    assert r.status_code == 200
    order_id = r.text.split()[-1]
    session = Session()
    order_website_from_db = session.query(OrderWebsite) \
        .filter_by(id=order_id).first()
    start_time = time.time()

    while order_website_from_db.order_status == False:
        if time.time() - start_time > 10:
            break
        session.commit()

    assert time.time() - start_time < 10
    assert order_website_from_db.order_status
    website_images_from_db = session.query(WebsiteImage) \
        .filter_by(order_id=order_id).all()
    assert len(website_images_from_db) != 0
    url = f'http://api:5000/pickup_order/{order_id}'
    r = requests.get(url)
    zip_path = f'images_{order_id}.zip'

    with open(zip_path, 'wb') as zip_file:
        zip_file.write(r.content)

    zip_file.close()
    zip_file_response = zipfile.ZipFile(zip_path, 'r')
    os.remove(zip_path)
    zip_file_namelist = zip_file_response.namelist()

    for website_image in website_images_from_db:
        assert website_image.img_type in supported_img_types
        img_ext = supported_img_types[website_image.img_type]
        image_name = f'img_{website_image.id}.{img_ext}'
        assert image_name in zip_file_namelist
        session.delete(website_image)

    session.delete(order_website_from_db)
    session.commit()
    session.close()

