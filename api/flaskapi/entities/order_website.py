from sqlalchemy import (
    Column,
    Integer,
    VARCHAR,
    DateTime,
    Boolean
)
import datetime
from sqlalchemy.orm import relationship

from flaskapi.entities.base import Base

class OrderWebsite(Base):
    __tablename__ = 'order_website'
 
    id = Column(Integer, primary_key=True)
    website_url = Column(VARCHAR(length=100))
    order_type = Column(VARCHAR(length=32))
    data_time = Column(DateTime, default=datetime.datetime.utcnow)
    order_status = Column(Boolean, default=False)
    website_images = relationship("WebsiteImage", back_populates="order_website")
    website_content = relationship("WebsiteContent", 
        uselist=False, back_populates="order_website")

    def __repr__(self):
        return f"<OrderWebsite(id='{self.id}'," \
            f"website_url='{self.website_url}'," \
            f"order_type='{self.order_type}'," \
            f"data_time='{self.data_time}'," \
            f"order_status='{self.order_status}')>"
