#!/usr/bin/env python
from datetime import datetime
from sqlalchemy import Column, Table, DateTime, Boolean
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import check_password_hash
from werkzeug import generate_password_hash

Base = declarative_base()


# Flask/SQLAlchemy ORM mappings for the objects we store in the DB

class User(Base):
    """A user login, with credentials and authentication."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now,
                      onupdate=datetime.now)
    username = Column('username', String(200))
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)

    password = Column('password', String(100))
    company_id = Column(Integer, ForeignKey('company.company_id'))
    company_name = Column('company_name', String(100))
    # def _get_password(self):
    #     return self._password
    #
    # def _set_password(self, password):
    #     if password:
    #         password = password.strip()
    #         self._password = generate_password_hash(password)
    #         password_descriptor = property(_get_password,
    #                                _set_password)
    #         password = synonym('_password',
    #                            descriptor=password_descriptor)
    #
    # def check_password(self, password):
    #     if self.password is None:
    #         return False
    #     password = password.strip()
    #     if not password:
    #         return False
    #     return check_password_hash(self.password, password)
    #
    # @classmethod
    # def authenticate(cls, query, email, password):
    #     email = email.strip().lower()
    #     user = query(cls).filter(cls.email == email).first()
    #     if user is None:
    #         return None, False
    #     if not user.active:
    #         return user, False
    #     return user, user.check_password(password)


class CompanyVN(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    company_name = Column(Text)
    users = relationship("User", backref="company")
    # one to many unidirectional relationship
    sprints = relationship("SprintVN", backref="company")


# table for the many to many relationship between userstories and sprints
us_sprint_association_table = Table('us_sprint_association', Base.metadata,
                                    Column('sprint_id', Integer, ForeignKey('sprint.sprint_id')),
                                    # Column('userstory_id', Integer, ForeignKey('userstory.userstory_id'))
                                    Column('id', Integer, ForeignKey('userstory.id'))
                                    )


class SprintVN(Base):
    __tablename__ = 'sprint'

    sprint_id = Column(Integer, primary_key=True)
    sprint_name = Column(Text)
    company_name = Column(Text)
    company_id = Column(Integer, ForeignKey('company.company_id'))


# table for the many to many relationship between userstories and concepts (classes)
us_class_association_table = Table('us_class_association', Base.metadata,
                                   # Column('userstory_id', Integer, ForeignKey('userstory.userstory_id')),
                                   Column('userstory_id', Integer, ForeignKey('userstory.id')),
                                   Column('class_id', Integer, ForeignKey('class.class_id'))
                                   )

#  table for the many to many relationship between userstories and relationships
us_relationship_association_table = Table('us_relationship_association', Base.metadata,
                                          Column('userstory_id', Integer, ForeignKey('userstory.id')),
                                          Column('relationship_id', Integer, ForeignKey('relationship.relationship_id'))
                                          )


class UserStoryVN(Base):
    """A UserStory """
    __tablename__ = 'userstory'

    id = Column(Integer, primary_key=True)
    userstory_id = Column(Integer)
    text = Column(Text)
    no_punct = Column(Text)
    role = Column(Text)
    means = Column(Text)
    means_verb = Column(Text)
    means_object = Column(Text)
    functional_role = Column(Text)
    ends = Column(Text)
    in_sprint = Column(Integer)

    # many to one relationship
    sprints = relationship("SprintVN", cascade="delete",
                           secondary=us_sprint_association_table, backref="userstorysprints", lazy='dynamic')
    # many to many relationship
    classes = relationship("ClassVN", cascade="delete",
                           secondary=us_class_association_table, backref="userstories", lazy='dynamic')
    # many to many relationship
    relationships = relationship("RelationShipVN", cascade="delete",
                                 secondary=us_relationship_association_table, backref="relationships", lazy='dynamic')


class ClassVN(Base):
    __tablename__ = 'class'

    class_id = Column(Integer, primary_key=True)
    class_name = Column(Text)
    parent_name = Column(Text)
    weight = Column(Integer)
    group = Column(Text)
    cluster = Column(Integer)


class RelationShipVN(Base):
    """A Relationship between two objects between user stories """
    __tablename__ = 'relationship'

    relationship_id = Column(Integer, primary_key=True)
    relationship_domain = Column(Text)
    relationship_name = Column(Text)
    relationship_range = Column(Text)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create the database
engine = create_engine('sqlite:///app.db', echo=True)
# create the tables with the engine
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
