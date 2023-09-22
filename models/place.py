#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models import storage_type
from models.amenity import Amenity
from models.review import Review


place_amenity = Table("place_amenity", Base.metadata, Column(
                      "place_id", String(60), ForeignKey('places.id'),
                      primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                      ForeignKey('amenities.id'), primary_key=True,
                      nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if storage_type == "db":

        city_id = Column(String(60), ForeignKey('cities.id'),
                         nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary='place_amenity',
                                 viewonly=False,
                                 back_populates="place_amenities")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Get reviews associated with a place"""
            from models import storage
            place_reviews = []
            all_reviews = storage.all(Review)
            for item in all_reviews.values():
                if item.place_id == self.id:
                    place_reviews.append(item)
            return place_reviews

        @property
        def amenities(self):
            """
            Getter to retrieve amenities based on
            the attribute amenity_ids that contains all
            Amenity.id.
            """
            from models import storage
            return [storage.all(Amenity).get(amenity_id)
                    for amenity_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """
            Setter for adding an Amenity.id to the
            amenity_ids attribute.
            """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
