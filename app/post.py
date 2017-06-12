#!/usr/bin/env python
import sys

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc, and_
from models import Base, ClassVN, UserStoryVN, RelationShipVN, SprintVN, engine
from form import SetInfoForm
import pdb

sys.path.insert(0, '/home/gjslob/Documents/environments/inarrator/VisualNarrator')
# from post import poster # the function to add the stuff to the database
form = SetInfoForm()
# create a session with the engine from models.py
Session = sessionmaker(bind=engine)
session = Session()

# from app.UserStory import UserStory


# this function is defined here because it could not be properly used through importing it from
# VisualNarrator.Utility
def occurence_list(li):
    res = []
    for o in li:
        if str(o) not in res and o >= 0:
            res.append(str(o))
    if res:
        return ', '.join(res)
    return "Doesn not occur, deducted"


# # get the starting position for the new userstory IDs, based on the presence/absence of
# # user stories already in the database
# starting_id = session.query(UserStoryVN).order_by(UserStoryVN.id.desc()).first()
# if starting_id is None:
#     starting_id = 0
# else:
#     starting_id = starting_id.id
# print('FIRST STARTING_ID', starting_id.id)


def add_userstories(us_instances, form_data):
    # add the user stories (us_vn) in the us_instances object to the database
    for us_vn in us_instances:
        # each user story has a functional role part, a means part and a means_main part.
        # extract those
        func_role = str(us_vn.role.functional_role.main)
        means_main_verb = str(us_vn.means.main_verb.main)
        means_main_object = str(us_vn.means.main_object.main)
        us_entry = UserStoryVN(userstory_id=us_vn.number, text=us_vn.text, no_punct=us_vn.sentence,
                               role=us_vn.role.indicator, means=us_vn.means.indicator, means_verb=means_main_verb,
                               means_object=means_main_object, functional_role=func_role, ends=us_vn.ends.indicator,
                               in_sprint=form_data['sprint_id'])
        # add a new user story entry to the database
        session.add(us_entry)
        # get the sprint ID from the databse equal to the one the user has entered in the
        # sprint ID form field for this set of user stories
        sprint = session.query(SprintVN).get(form_data['sprint_id'])
        #  then add the many to many relationship for this set of stories
        # with this sprint ID in the sprints-userstories association table
        us_entry.sprints.append(sprint)

    session.commit()


def add_concepts(output_ontobj, m, starting_id):

    # Now find the user story with the highest ID in the database
    # and use this ID as a startingpoint for new UserStory.ID's
    highest_id = session.query(UserStoryVN).order_by(UserStoryVN.id.desc()).first()
    print('FIRST HIGHEST ID', highest_id)
    # Now add the concepts (class_vn) to a list of dicts (concepts_list) from the classes which will become nodes

    concepts_list = []
    excluded_concepts_list = []
    # get the list of concepts and their weights.
    # Not all concepts in output_ontobj.classes have a weight of 0> and not are in the weights dict
    weights_dict = dict(m['sum'].copy().reset_index().sort_values(['sum'], ascending=False).values.tolist())
    print(weights_dict, 'WEIGHTS DICT')
    all_classes_list = []
    concepts_with_weight = []
    for class_vn in output_ontobj.classes:
        one_concept = {'class_name': class_vn.name, 'parent_name': class_vn.parent,
                       'occurs_in': occurence_list(class_vn.stories), 'weight': '0', 'group': class_vn.is_role}
        all_classes_list.append(one_concept)
        # if cl is not is_us:

        # ....else add it with the name and weight from the weights_dict

        # if key == class_vn.name:
    for concept in all_classes_list:
        for key, value in weights_dict.items():
            if concept['class_name'] == key:
                concept['weight'] = value

    # now add the concepts from the concepts_list to the database
    print('ALL_CLASSES_LIST', all_classes_list)

    for class_vn in all_classes_list:

        class_entry = ClassVN(class_name=class_vn['class_name'],
                              parent_name=class_vn['parent_name'], weight=class_vn['weight'], group=class_vn['group'],
                              cluster='')

        session.add(class_entry)

        try:
            session.commit()

        # except exc.IntegrityError as e:
        except Exception as e:
            print('EXCEPTION:', e)
            session.rollback()
            excluded_concepts_list.append(class_vn)
        # else:
        #     break

        # session.commit()

        # WHAT HAPPENS HERE ???????????????????????????
        list_of_us_ids = class_vn['occurs_in']
        class_from_db = session.query(ClassVN).filter_by(class_name=class_vn['class_name']).first()
        class_id = class_from_db.class_id
        print('#########', class_id, class_from_db.class_name)

        #  check all user story ids in the list

        print('$$$$$$$$$$$$', list_of_us_ids)
        # each class/concept is part of one of more user stories
        # this information is located in the relationship.list_of_us_ids property
        for us_id in list_of_us_ids.split(', '):
            # find the user story that is in the list_of_us_ids by .userstory_id
            # and find it with .id as well so we find only the stories in this particular set
            us = session.query(UserStoryVN).filter(and_(UserStoryVN.id > starting_id, UserStoryVN.id <= highest_id.id,
                                                        UserStoryVN.userstory_id == us_id)).first()
            print('%%%%%%%%%%', us.id, us.no_punct)
            print('^^^^HIGHEST_ID', highest_id.id, highest_id.no_punct)
            cl = session.query(ClassVN).get(class_id)
            print('#######CLASS_ID#########', cl.class_name, cl.class_id)
            #  add a class to the relationship named ' classes' on the userstory table
            # association table will automatically be filled this way

            us.classes.append(cl)
        session.commit()
    print('******EXCLUDED CONCEPTS******', excluded_concepts_list)
    # import pdb
    # pdb.set_trace()

def add_relationships(output_prologobj, starting_id):

    highest_id = session.query(UserStoryVN).order_by(UserStoryVN.id.desc()).first()
    # then add relationships between concepts (ClassVNs) which will become edges
    # if there are already entries in the database, get the highest id as
    # a starting point for the new relationships
    relationships_output = output_prologobj.relationships
    for relationship in relationships_output:
        # take a relationship and add it
        rel_entry = RelationShipVN(relationship_domain=relationship.domain,
                                   relationship_name=relationship.name, relationship_range=relationship.range)
        try:
            session.add(rel_entry)
            session.commit()
        except Exception as e:
            print('Exception raised', e)

        # access the ontology object property "relationship.stories" which stores
        # the user story ids in which the relationshsip occurs
        list_of_us_ids = relationship.stories
        # get the newest relationship (with the highest relationship_id) which should be the one just added
        relationship_from_db = session.query(RelationShipVN).order_by(RelationShipVN.relationship_id.desc()).first()
        relationship_id = relationship_from_db.relationship_id
        # each relationship is part of one of more user stories
        # this information is located in the relationship.list_of_us_ids property
        seen = set()
        uniq = []
        for x in list_of_us_ids:
            if x not in seen:
                uniq.append(x)
                seen.add(x)
        for us_id in uniq:
            # find the user story that is in the list_of_us_ids by .userstory_id
            # and find it with .id as well so we find only the stories in this particular set
            us = session.query(UserStoryVN).filter(and_(UserStoryVN.id > starting_id, UserStoryVN.id <= highest_id.id,
                                                        UserStoryVN.userstory_id == us_id)).first()
            # rel = session.query(RelationShipVN).get(relationship_id) REDUNDANT!!!
            #  add a class to the relationship named ' classes' on the userstory table
            # association table will automatically be filled this way
            us.relationships.append(relationship_from_db)
            # import pdb
            # pdb.set_trace()
    session.commit()

def add_data_to_db(us_instances, output_ontobj, output_prologobj, m, form_data):
    # get the starting position for the new userstory IDs, based on the presence/absence of
    # user stories already in the database
    starting_id = session.query(UserStoryVN).order_by(UserStoryVN.id.desc()).first()
    if starting_id is None:
        starting_id = 0
    else:
        starting_id = starting_id.id
    print('FIRST STARTING_ID', starting_id)

    add_userstories(us_instances, form_data)
    add_concepts(output_ontobj, m, starting_id)
    add_relationships(output_prologobj, starting_id)

    # import pdb;pdb.set_trace()
    # session.commit()
