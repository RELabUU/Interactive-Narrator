#!/usr/bin/env python
import sys
import os
import math
from _operator import and_

sys.path.append('/home/gjslob/Documents/environments/inarrator')

from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, not_, or_
from flask import Flask, jsonify, render_template, url_for, request, flash, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename, redirect
from collections import OrderedDict
from models import Base
from form import SetInfoForm
import json
from post import poster


sys.path.append('/home/gjslob/Documents/environments/inarrator/VisualNarrator')
from VisualNarrator import run
from models import UserStoryVN, RelationShipVN, ClassVN, CompanyVN, \
    SprintVN, engine, us_class_association_table, \
    us_relationship_association_table, \
    us_sprint_association_table

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
UPLOAD_FOLDER = 'uploads'

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

db = SQLAlchemy(app)
db.Model = Base

# Base = declarative_base()
# engine = create_engine('sqlite:///../VisualNarrator_v2/app.db', echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()


#  route for getting the form info (company/sprint) and putting it into the database
@app.route('/form', methods=['GET', 'POST'])
def form():
    form = SetInfoForm(request.form)

    if request.method == 'POST' and form.validate():
        form_data = {}
        form_data['company_id'] = form.company_id.data
        form_data['company_name'] = form.company_name.data
        form_data['sprint_id'] = form.sprint_id.data
        form_data['sprint_name'] = form.sprint_name.data
        #  if company name and id are supplied store them in DB

        session.add(CompanyVN(company_id=form.company_id.data, company_name=form.company_name.data))
        # session.add(CompanyVN(company_id='1', company_name='abc'))

        session.add(SprintVN(sprint_id=form.sprint_id.data, sprint_name=form.sprint_name.data,
                             company_name=form.company_name.data, company_id=form.company_id.data))
        # session.add(SprintVN(sprint_id='12', sprint_name='sprint1', company_name='abc', company_id='1'))
        session.commit()
        # run the visual narrator back-end and obtain needed objects for visualization
        data = run.program('example_stories.txt')
        #  run the poster method to place the objects and their attributes in the database
        poster(data['us_instances'], data['output_ontobj'], data['output_prologobj'], data['matrix'], form_data)

        # redirect the user to the visualization directly
        return redirect(url_for('index'))

    flash('not valid')
    return render_template('form.html', form=form)


# get the roles to populate the multiselect with javascript
@app.route('/getroles')
def get_roles():
    functional_roles = session.query(UserStoryVN.functional_role.distinct().label("functional_role"))
    all_roles = [row.functional_role for row in functional_roles.all()]
    print(all_roles)
    return jsonify(all_roles)


# get the sprints to populate the multiselect with javascript
@app.route('/getsprints')
def get_sprints():
    sprints = session.query(SprintVN.sprint_id.distinct().label("sprint_id"))
    all_sprints = [row.sprint_id for row in sprints.all()]
    print(all_sprints)
    return jsonify(all_sprints)


# this is the main query that queries the database for concepts and relationships basd on the
# roles and sprints that were selected by the user
#
# This function returns an array of nodes that are
# connected (i.e. occur in a user story where the role occurs in) to the selected role.
@app.route('/query')
def get_test():
    checked_roles = json.loads(request.args.get('roles'))
    checked_sprints = json.loads(request.args.get('sprints'))

    classes = session.query(ClassVN) \
        .join(us_class_association_table) \
        .join(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .filter(and_(
        UserStoryVN.functional_role.in_(checked_roles)),
        (SprintVN.sprint_id.in_(checked_sprints))
    ) \
        .all()

    nodes = [{"label": cl.class_name, "weight": cl.weight, "id": cl.class_id} for cl in classes]

    class_names = [cl.class_name for cl in classes]

    class_name_id_map = {cl.class_name: cl.class_id for cl in classes}

    class_relationships = session.query(RelationShipVN) \
        .join(us_relationship_association_table) \
        .join(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .filter(
        or_(RelationShipVN.relationship_domain.in_(class_names),
            RelationShipVN.relationship_range.in_(class_names))
    ) \
        .filter(and_(
        UserStoryVN.functional_role.in_(checked_roles)),
        (SprintVN.sprint_id.in_(checked_sprints))
    ) \
        .all()

    edges = []
    for class_relationship in class_relationships:
        try:
            edges.append({
                "id": class_relationship.relationship_id,
                "from": class_name_id_map[class_relationship.relationship_domain],
                "to": class_name_id_map[class_relationship.relationship_range],
                "label": class_relationship.relationship_name
            })
        except KeyError:
            print("Impossible relationship: %s -> %s -> %s" % (
            class_relationship.relationship_domain, class_relationship.relationship_name,
            class_relationship.relationship_range))
            pass

    return jsonify(nodes=nodes, edges=edges)


# a route for displaying the visualization
@app.route('/visjs', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# a route for the uploading of user story sets
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html')


# redirect the user to the uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


# a route for delivering the list of concepts to be made into nodes
@app.route('/concepts')
def concepts():
    # first apply the "Role" mark to each concept that is a functional_role:
    all_roles = session.query(ClassVN).filter(ClassVN.group == '1').all()

    for role in all_roles:
        role.group = "Role"
        session.commit()
    # now jsonify and return the concepts to the fore-end
    concepts_query = select([ClassVN])
    concept_list = []
    concepts_query_res = conn.execute(concepts_query)
    for c in concepts_query_res:
        weight2 = 15 + (3 * math.sqrt(c.weight))
        concept_dictionary = {'id': c.class_id, 'label': c.class_name, 'weight': c.weight, 'size': weight2,
                              'group': c.group}


        concept_list.append(concept_dictionary)

    json_concepts = json.dumps(concept_list)
    return json_concepts


@app.route('/relationships')
def relationships():
    concepts_query = select([ClassVN])
    relationships_query = select([RelationShipVN])
    relsresult = conn.execute(relationships_query)
    concepts_query_res = conn.execute(concepts_query)
    edges_id_list = []
    concepts_dict = {}
    edges_id_dict = {}
    concepts_dict_list = []

    for concept in concepts_query_res:
        concepts_dict[concept.class_id] = concept.class_name
        concepts_dict_list.append([concept.class_id, concept.class_name])

    # check if a domain(from) or range(to) is part of the us concepts and if so make
    # the relationship between the concepts involved
    for re in relsresult:
        # for sublist in concepts_dict_list:
        for key, value in concepts_dict.items():
            if value == re.relationship_domain:
                x = key
        for key, value in concepts_dict.items():
            if value == re.relationship_range:
                y = key

        edges_id_dict = {'id': re.relationship_id, 'from': x, 'to': y, 'label': re.relationship_name}
        edges_id_list.append(edges_id_dict)

    json_edges = json.dumps(edges_id_list)

    return json_edges


if __name__ == '__main__':
    app.run()
