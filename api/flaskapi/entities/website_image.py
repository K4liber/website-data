from flaskapi.entities.base import Base
from sqlalchemy import (
    Column,
    Integer,
    VARCHAR,
    BLOB,
    ForeignKey
)
from sqlalchemy.orm import relationship

class WebsiteImage(Base):
    __tablename__ = 'website_image'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order_website.id'))
    order_website = relationship("OrderWebsite", back_populates="website_images")
    caption = Column(VARCHAR(length=45))
    img = Column(BLOB)

    def __repr__(self):
        return f"<WebsiteImage(id='{self.id}'," \
            f"order_id='{self.order_id}'," \
            f"caption='{self.caption}')>"
