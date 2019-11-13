from flaskapi.entities.base import Base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    TEXT
)
from sqlalchemy.orm import relationship


class WebsiteContent(Base):
    __tablename__ = 'website_content'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order_website.id'))
    order_website = relationship("OrderWebsite",
                                 back_populates="website_content")
    content = Column(TEXT())

    def __repr__(self):
        return f"<WebsiteContent(id='{self.id}'," \
            f"order_id='{self.order_id}'," \
            f"content='{self.content}')>"

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'content': self.content
        }
