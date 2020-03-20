# coding: utf-8
from sqlalchemy import Column, Float, ForeignKey, String, Table, Text, exists
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

engine = create_engine('mysql://user:password@127.0.0.1/db')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

Base = declarative_base()
metadata = Base.metadata


class ItemStat(Base):
    __tablename__ = 'item_stats'

    item_id = Column(INTEGER(11), primary_key=True, unique=True)
    item_importance = Column(Float)
    item_views = Column(INTEGER(11))
    item_grabs = Column(INTEGER(11))
    item_shares = Column(INTEGER(11))
    item_ikes = Column(INTEGER(11))
    item_in_collections = Column(INTEGER(11))
    item_audio_play_count = Column(INTEGER(11))


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(INTEGER(11), primary_key=True, unique=True)
    item_title = Column(Text)
    item_type = Column(Text)
    item_medium = Column(Text)
    item_creator_name = Column(Text)
    item_creator_artist_codename = Column(Text)
    item_created = Column(Text)
    item_description_short = Column(Text)
    item_description_long = Column(Text)
    item_height = Column(Text)
    item_width = Column(Text)
    item_image_preview_url = Column(Text)
    item_image_large_url = Column(Text)
    item_api_source_id = Column(String(200))
    item_api_source = Column(Text)
    item_source_url = Column(Text)

    @staticmethod
    def exists_with_source_id(api_source_id):
        return session.query(exists().where(Item.item_api_source_id == api_source_id)).scalar()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(INTEGER(11), primary_key=True, unique=True)
    user_api_key = Column(String(45), unique=True)
    user_facebook_id = Column(String(45), unique=True)
    user_steam_id = Column(String(45), unique=True)
    user_epic_id = Column(String(45), unique=True)
    user_email = Column(String(45), unique=True)
    user_password = Column(Text)
    user_name = Column(Text)


class UserCollection(Base):
    __tablename__ = 'user_collections'

    collection_id = Column(INTEGER(11), primary_key=True, unique=True)
    user_id = Column(ForeignKey('users.user_id'), nullable=False, index=True)
    collection_name = Column(String(45), nullable=False)

    user = relationship('User')


t_collection_items = Table(
    'collection_items', metadata,
    Column('collection_id', ForeignKey('user_collections.collection_id'), nullable=False, index=True),
    Column('item_id', INTEGER(11), nullable=False),
    Column('collection_name', Text)
)
