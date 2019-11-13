from flaskapi.entities.base import Base
from sqlalchemy import (
    Column,
    Integer,
    TEXT,
    BLOB,
    VARCHAR,
    ForeignKey
)
from sqlalchemy.orm import relationship


class WebsiteImage(Base):
    __tablename__ = 'website_image'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order_website.id'))
    order_website = relationship("OrderWebsite",
                                 back_populates="website_images")
    caption = Column(TEXT())
    img = Column(BLOB)
    img_type = Column(VARCHAR(15))

    def __repr__(self):
        return f"<WebsiteImage(id='{self.id}'," \
            f"order_id='{self.order_id}'," \
            f"img_type='{self.img_type}'," \
            f"caption='{self.caption}')>"

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'caption': self.caption,
            'img_type': self.img_type,
            'img': self.img
        }
