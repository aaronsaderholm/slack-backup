"""
Convinient object mapping from slack API reponses
"""
from datetime import datetime

from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from slack_backup.db import Base


class Purpose(Base):
    __tablename__ = 'purposes'

    id = Column(Integer, primary_key=True)
    last_set = Column(DateTime)
    value = Column(Text)

    creator_id = Column(Integer, ForeignKey('users.id'), index=True)
    creator = relationship("User", back_populates="purposes")

    channel_id = Column(Integer, ForeignKey('channels.id'), index=True)
    channel = relationship("Channel", back_populates="purpose")

    def __init__(self, data_dict=None):
        self.update(data_dict)

    def update(self, data_dict):
        data_dict = data_dict or {}
        self.last_set = datetime.fromtimestamp(data_dict.get('last_set', 0))
        self.value = data_dict.get('value')

    def __repr__(self):
        return u'<%s %s>' % (str(hex(id(self))), self.__unicode__())

    def __unicode__(self):
        return u', %s %s' % (self.id, self.value)


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    last_set = Column(DateTime)
    value = Column(Text)

    channel_id = Column(Integer, ForeignKey('channels.id'), index=True)
    channel = relationship("Channel", back_populates="topic")

    creator_id = Column(Integer, ForeignKey('users.id'), index=True)
    creator = relationship("User", back_populates="topics")

    def __init__(self, data_dict=None):
        self.update(data_dict)

    def update(self, data_dict):
        data_dict = data_dict or {}
        self.last_set = datetime.fromtimestamp(data_dict.get('last_set', 0))
        self.value = data_dict.get('value')

    def __repr__(self):
        return u'<%s %s>' % (str(hex(id(self))), self.__unicode__())

    def __unicode__(self):
        return u', %s %s' % (self.id, self.value)


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    slackid = Column(Text)
    name = Column(Text)
    created = Column(DateTime)
    is_archived = Column(Boolean, default=False)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True,
                        index=True)
    creator = relationship("User", back_populates="channels")

    purpose = relationship("Purpose", uselist=False, back_populates="channel")
    topic = relationship("Topic", uselist=False, back_populates="channel")

    def __init__(self, data_dict=None):
        self.update(data_dict)

    def update(self, data_dict):
        data_dict = data_dict or {}

        self.slackid = data_dict.get('id', '')
        self.name = data_dict.get('name', '')
        self.created = datetime.fromtimestamp(data_dict.get('created', 0))
        self.is_archived = data_dict.get('is_archived', False)

    def __repr__(self):
        return u'<%s %s>' % (str(hex(id(self))), self.__unicode__())

    def __unicode__(self):
        return u'%s, %s %s' % (self.__class__.__name__, self.id, self.name)


class UserProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    avatar_hash = Column(Text)
    email = Column(Text)
    first_name = Column(Text)
    image_192 = Column(Text)
    image_24 = Column(Text)
    image_32 = Column(Text)
    image_48 = Column(Text)
    image_72 = Column(Text)
    image_original = Column(Text)
    last_name = Column(Text)
    real_name = Column(Text)
    real_name_normalized = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="profile")

    def __init__(self, data_dict=None):
        self.update(data_dict)

    def update(self, data_dict):
        data_dict = data_dict or {}

        self.avatar_hash = data_dict.get('avatar_hash', '')
        self.email = data_dict.get("email", '')
        self.first_name = data_dict.get('first_name', '')
        self.image_192 = data_dict.get('image_192', '')
        self.image_24 = data_dict.get('image_24', '')
        self.image_32 = data_dict.get('image_32', '')
        self.image_48 = data_dict.get('image_48', '')
        self.image_72 = data_dict.get('image_72', '')
        self.image_original = data_dict.get('image_original', '')
        self.last_name = data_dict.get('last_name', '')
        self.real_name = data_dict.get('real_name', '')
        self.real_name_normalized = data_dict.get('real_name_normalized', '')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False)
    name = Column(Text)
    real_name = Column(Text)
    slackid = Column(Text)

    channels = relationship("Channel", back_populates="creator")
    profile = relationship("UserProfile", uselist=False, back_populates="user")
    purposes = relationship("Purpose", back_populates="creator")
    topics = relationship("Topic", back_populates="creator")

    def __init__(self, data_dict=None):
        self.update(data_dict)

    def update(self, data_dict=None):
        data_dict = data_dict or {}

        self.deleted = data_dict.get('deleted', False)
        self.name = data_dict.get("name", '')
        self.real_name = data_dict.get('real_name', '')
        self.slackid = data_dict.get('id', '')

        if not self.profile:
            self.profile = UserProfile(data_dict.get('profile'))
        else:
            self.profile.update(data_dict.get('profile'))

    def __repr__(self):
        return u'<%s %s>' % (str(hex(id(self))), self.__unicode__())

    def __unicode__(self):
        return u'%s, %s %s' % (self.__class__.__name__, self.id, self.name)


class Reactions(object):
    def __init__(self, data_dict=None):
        data_dict = data_dict or {}


class Messages(object):
    def __init__(self, data_dict=None):
        data_dict = data_dict or {}

        self.ts = data_dict.get('ts', '')
        self.user_id = data_dict.get('user', '')
        self.type = data_dict.get('type', '')
        self.text = data_dict.get('text', '')
        self.reactions = Reactions(data_dict.get('reactions', ''))
