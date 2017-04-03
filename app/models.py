#!/usr/bin/env python
from sqlalchemy import Boolean, Column, Table
from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Flask/SQLAlchemy ORM mappings for the objects we store in the DB


class CompanyVN(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    company_name = Column(Text)
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
    sprints = relationship("SprintVN",
                           secondary=us_sprint_association_table, backref="userstorysprints", lazy='dynamic')
    # many to many relationship
    classes = relationship("ClassVN",
                           secondary=us_class_association_table, backref="userstories", lazy='dynamic')
    # many to many relationship
    relationships = relationship("RelationShipVN",
                                 secondary=us_relationship_association_table, backref="relationships", lazy='dynamic')


class ClassVN(Base):
    __tablename__ = 'class'

    class_id = Column(Integer, primary_key=True)
    class_name = Column(Text)
    parent_name = Column(Text)
    weight = Column(Integer)
    group = Column(Text)


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
