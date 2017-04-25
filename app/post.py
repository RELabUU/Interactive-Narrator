#!/usr/bin/env python
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from models import Base, ClassVN, UserStoryVN, RelationShipVN, SprintVN, engine
from form import SetInfoForm

# from app.utility import occurence_list
sys.path.insert(0, '/home/gjslob/Documents/environments/inarrator/VisualNarrator')
# from post import poster # the function to add the stuff to the database
form = SetInfoForm()
# create a session with the engine from models.py
Session = sessionmaker(bind=engine)
session = Session()


# from app.UserStory import UserStory


# this function is defined here because it could not be properly used through importing it from Utility
def occurence_list(li):
    res = []
    for o in li:
        if str(o) not in res and o >= 0:
            res.append(str(o))
    if res:
        return ', '.join(res)
    return "Doesn not occur, deducted"


def poster(us_instances, output_ontobj, output_prologobj, m, form_data):
    starting_id = session.query(UserStoryVN).order_by(UserStoryVN.id.desc()).first()
    if starting_id is None:
        starting_id = 0
    else:
        starting_id = starting_id.id

    # add the user stories (us_vn) to the database
    for us_vn in us_instances:
        func_role = str(us_vn.role.functional_role.main)
        means_main_verb = str(us_vn.means.main_verb.main)
        means_main_object = str(us_vn.means.main_object.main)
        us_entry = UserStoryVN(userstory_id=us_vn.number, text=us_vn.text, no_punct=us_vn.sentence,
                               role=us_vn.role.indicator, means=us_vn.means.indicator, means_verb=means_main_verb,
                               means_object=means_main_object, functional_role=func_role, ends=us_vn.ends.indicator,
                               in_sprint=form_data['sprint_id'])
        session.add(us_entry)
        #  add the many to many relationship for sprints-userstories
        sprint = session.query(SprintVN).get(form_data['sprint_id'])
        us_entry.sprints.append(sprint)

    highest_id = session.query(UserStoryVN).order_by(UserStoryVN.id.desc()).first()

    # then add relationships between concepts - which will become edges - too
    # if there are already entries in the database, get the highest id as starting point
    relationships_output = output_prologobj.relationships
    for relationship in relationships_output:
        rel_entry = RelationShipVN(relationship_domain=relationship.domain,
                                   relationship_name=relationship.name, relationship_range=relationship.range)
        session.add(rel_entry)
        session.commit()
        # access the ontology object property "stories" which stores
        # the story ids in which the relationshsip occurs
        list_of_us_ids = relationship.stories
        relationship_from_db = session.query(RelationShipVN).order_by(RelationShipVN.relationship_id.desc()).first()
        relationship_id = relationship_from_db.relationship_id

        for us_id in list_of_us_ids:
            us = session.query(UserStoryVN).filter(and_(UserStoryVN.id > starting_id, UserStoryVN.id <= highest_id.id,
                                                        UserStoryVN.userstory_id == us_id)).first()
            rel = session.query(RelationShipVN).get(relationship_id)
            #  add a class to the relationship named ' classes' on the userstory table
            # association table will automatically be filled this way
            us.relationships.append(rel)
    session.commit()

    # add the concepts (class_vn) to a list of dicts from the classes which will become nodes
    i = 0
    concepts_list = []
    weights_dict = dict(m['sum'].copy().reset_index().sort_values(['sum'], ascending=False).values.tolist())
    for class_vn in output_ontobj.classes:
        i = i + 1  # redundant! not used anymore see below
        # if cl is not is_us:   #ids are redundant because of auto_increment!
        if class_vn.name not in weights_dict.keys():
            concepts_dict = {'class_id': i, 'class_name': class_vn.name, 'parent_name': class_vn.parent,
                             'occurs_in': occurence_list(class_vn.stories), 'weight': '0', 'group': class_vn.is_role}
            concepts_list.append(concepts_dict)
        else:
            for key, value in weights_dict.items():
                if key == class_vn.name:
                    concepts_dict2 = {'class_id': i, 'class_name': class_vn.name, 'parent_name': class_vn.parent,
                                      'occurs_in': occurence_list(class_vn.stories), 'weight': value,
                                      'group': class_vn.is_role}
                    concepts_list.append(concepts_dict2)
    # NOTICE: class_id is stored in the dictionaries but not used because an ID is added by SQLLite automatically
    for class_vn in concepts_list:

        class_entry = ClassVN(class_name=class_vn['class_name'],
                              parent_name=class_vn['parent_name'], weight=class_vn['weight'], group=class_vn['group'],
                              cluster='')
        session.add(class_entry)
        session.commit()

        # add the reationships between sprints and userstories (association table: us_class_association_table)
        list_of_us_ids = class_vn['occurs_in']
        class_from_db = session.query(ClassVN).filter_by(class_name=class_vn['class_name']).first()
        class_id = class_from_db.class_id
        # get the highest unique ID as starting point  so that each userstory_id (a VN generated id)
        # points to a unique userstory: a userstory in the new set
        #  check all user story ids in the list
        for us_id in list_of_us_ids.split(', '):
            us = session.query(UserStoryVN).filter(and_(UserStoryVN.id > starting_id, UserStoryVN.id <= highest_id.id,
                                                        UserStoryVN.userstory_id == us_id)).first()
            cl = session.query(ClassVN).get(class_id)
            #  add a class to the relationship named ' classes' on the userstory table
            # association table will automatically be filled this way
            us.classes.append(cl)

    session.commit()
