#!/usr/bin/env python
import sys
import os
import math
# from _operator import and_

# sys.path.append('/home/gjslob/Documents/environments/inarrator')
sys.path.append('/var/www/interactivenarrator')

from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, not_, or_
from flask import Flask, jsonify, render_template, url_for, request
from flask import flash, send_from_directory, Response, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename, redirect
from passlib.hash import sha256_crypt
from collections import OrderedDict
from models import Base, User
from form import SetInfoForm, LoginForm, RegistrationForm
import json
from post import add_data_to_db

# sys.path.append('/home/gjslob/Documents/environments/inarrator/VisualNarrator')
sys.path.append('/var/www/VisualNarrator')

from VisualNarrator import run
import VisualNarrator.run
from models import UserStoryVN, RelationShipVN, ClassVN, CompanyVN, \
    SprintVN, engine, us_class_association_table, \
    us_relationship_association_table, \
    us_sprint_association_table

# configuration
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

ALLOWED_EXTENSIONS = set(['txt', 'csv'])
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

db = SQLAlchemy(app)
db.Model = Base

# NOTE: sqlsession vs session usage!
# session is a login/logout session
# sqlsession is a Session() object

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sqlsession = Session()
conn = engine.connect()


@app.route('/')
def homepage():
    return render_template('index.html')

# # Homepage
# @app.route('/')
# def home():
#     if not session.get('logged_in'):
#         # return render_template('login.html')
#         return redirect(url_for('do_admin_login'))
#     else:
#         return redirect(url_for('show_dash'))
#         # return render_template('dashboard.html')


# a route for displaying the visualization
@app.route('/vis', methods=['GET', 'POST'])
def show_vis():
    # return render_template('vis.html')
    if session.get('logged_in'):
        return render_template('vis.html')
    else:
        return redirect(url_for('homepage'))


# registering a user
@app.route('/register', methods=['GET', 'POST'])
def do_register():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            company_name = form.company_name.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            # check if a user is new or existent...
            user_exists = sqlsession.query(User).filter(User.username == username).first()
            # ... if it exists, notify the user
            if user_exists:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)
            # ..else, create the new user and company
            else:
                new_user = User(username=username, company_name=company_name, email=email, password=password)
                sqlsession.add(new_user)
                sqlsession.add(CompanyVN(company_id='', company_name=company_name))

                sqlsession.commit()
                flash('thanks for registering')

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('show_dash'))

        return render_template("register.html", form=form)

    # except Exception as e:
    except:
        return render_template('register.html', form=form)
        # return(str(e))


# route for when the login form on the homepage is submitted
@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if not session.get('logged_in'):

        # try:
        if request.method == "POST":

            # form = LoginForm(request.form)
            POST_USERNAME = str(request.form['username'])
            POST_PASSWORD = str(request.form['password'])

            # query = sqlsession.query(User).filter(User.username.in_([POST_USERNAME]),
            #                                       User.password.in_([POST_PASSWORD]))
            # check if a user with the entered username exists
            check_user = sqlsession.query(User).filter(User.username.in_([POST_USERNAME]))

            user_exists = check_user.first()
            # print(user_exists.password)
            if user_exists:
                # flash('Wrong username/password, please try again')
                # if the password matches the username, log the user in
                if sha256_crypt.verify(POST_PASSWORD, user_exists.password):
                    print(check_user)
                # if check_user:
                    session['logged_in'] = True
                    flash('Thanks for logging in!')
                    print('succes')
                    return redirect(url_for('show_dash'))
                else:
                    flash('Sorry, wrong password/username')
                    print('failure')
                    return render_template('login.html')
            else:
                flash('Sorry, wrong password/username')
                return render_template('login.html')
    else:
        return redirect(url_for(show_dash))
        # return render_template('dashboard.html')

    # except:
    return redirect(url_for('show_dash'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template("login.html")

@app.route("/dashboard")
def show_dash():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        username = session['username']
        # show all the sprints that are in the database on the dashboard page
        all_sprints = sqlsession.query(SprintVN).all()
        sprints = [dict(sprint_id=sprint.sprint_id,
                        sprint_name=sprint.sprint_name,
                        company_id=sprint.company_id,
                        company_name=sprint.company_name) for sprint in all_sprints]

        return render_template("dashboard.html", sprints=sprints, username=username)

# View for clearing the entire database
@app.route("/cleandatabase")
def clean_database():
    # get all userstories and delete them one by one
    # the cascade makes sure all sprints, relationships, classes and association table entries are deleted as well
    userstoryVN = sqlsession.query(UserStoryVN).all()
    for userstory in userstoryVN:
        sqlsession.delete(userstory)
        # sqlsession.commit()

    try:
        sqlsession.commit()
        return redirect(url_for('show_dash'))
    except Exception as e:
        print('Exception raised', e)
        # import pdb
        # pdb.set_trace()
        sqlsession.rollback()
        return redirect(url_for('show_dash'))


# @app.route('/sprints/<int:sprint_id>/')
# def sprint_detail(sprint_id):
#     """Provide HTML page with a given sprint."""
#
#     # Query: get Appointment object by ID.
#     set = sqlsession.query(SprintVN).get(sprint_id)
#     if set is None:
#     # Abort with Not Found.
#         abort(404)
#
#     return render_template('set_detail.html',
#                            set=set)

@app.route('/form', methods=['GET', 'POST'])
def form():
    # use the form class from form.py
    form = SetInfoForm(request.form)
    # check who the active user is
    active_user = sqlsession.query(User).filter(User.username == session['username']).first()
    print(session['username'])
    # if the active user is identified, set the company name of that of the user's company
    if active_user:
        active_company_name = active_user.company_name
        active_company = sqlsession.query(CompanyVN).filter \
            (CompanyVN.company_name == active_company_name).first()

        # flash(session['username'])

    if request.method == 'POST' and form.validate():
        form_data = {}
        form_data['sprint_id'] = form.sprint_id.data
        form_data['sprint_name'] = form.sprint_name.data
        # check of the inserted sprint values already exist
        sprint_exists = sqlsession.query(SprintVN).filter\
            (SprintVN.sprint_name == form_data['sprint_name']).first()
        print('this sprint exists:', sprint_exists)
        # if the sprint already exists, notify the user...
        if sprint_exists:
            flash('sprint is already in the database')
            print('sprint exists already', sprint_exists)
            return redirect(url_for('form'))
        # ...if it doesn't, add it to the DB
        else:
            sqlsession.add(SprintVN(sprint_id=form_data['sprint_id'], sprint_name=form_data['sprint_name'],
                                    company_name=active_company_name, company_id=active_company.id))
            print('added sprint')
            # flash('sprint added')

        # FILE UPLOAD HANDLING
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('form'))
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            #     # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            #     # Move the file form the temporal folder to
            #     # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # set the filename so Visual Narrator can handle it
            set_filename = 'uploads/' + file.filename

            sqlsession.commit()
            # run the visual narrator back-end and obtain needed objects for visualization
            data = run.program(set_filename)
            #  run the poster method to place the objects and their attributes in the database
            # poster(data['us_instances'], data['output_ontobj'], data['output_prologobj'], data['matrix'], form_data)
            add_data_to_db(data['us_instances'], data['output_ontobj'], data['output_prologobj'], data['matrix'],
                           form_data)

            # if all went well redirect the user to the visualization directly
            return redirect(url_for('show_vis'))

    else:
        # flash('something went wrong, please try again')
        print('nothing was added to the database')
        return render_template('form.html', form=form)

    return render_template('form.html', form=form)

# get the roles to populate the multiselect with javascript
@app.route('/getroles')
def get_roles():
    functional_roles = sqlsession.query(UserStoryVN.functional_role.distinct().label("functional_role"))
    all_roles = [row.functional_role for row in functional_roles.all()]
    print(all_roles)
    return jsonify(all_roles)


# get the sprints to populate the multiselect with javascript
@app.route('/getsprints')
def get_sprints():
    sprints = sqlsession.query(SprintVN.sprint_id.distinct().label("sprint_id"))
    all_sprints = [row.sprint_id for row in sprints.all()]
    print(all_sprints)
    return jsonify(all_sprints)

# this route displays the userstories to which a node belongs when you click on the node
@app.route('/clickquery')
def click_query():
    clicked_nodes = json.loads(request.args.get('nodes'))
    print('NODES', clicked_nodes)
    node_userstory_list = []
    for one_node in clicked_nodes:
        print(one_node['id'])
        node_userstory = sqlsession.query(UserStoryVN).join(us_class_association_table)\
            .join(ClassVN).filter(ClassVN.class_id == one_node['id']).all()
        print('INFO', node_userstory)
        # node_info = sqlsession.query(ClassVN).filter(ClassVN.class_id == one_node['id']).one()
        # print('INFO', node_info)
        if node_userstory:
            node_userstory_list = [{"id": us.userstory_id,"text":us.text,"in sprint":us.in_sprint} for us in node_userstory]
        else:
            node_userstory_list = []
        print('NODEINFO', node_userstory_list)
    return jsonify(node_userstory_list)
    # return Response(json.dumps(node_userstory_list), mimetype='application/json')


# this is the main query that queries the database for concepts and relationships basd on the
# roles and sprints that were selected by the user

# This function returns an array of nodes that are
# connected (i.e. occur in a user story where the role occurs in) to the selected role.
@app.route('/query')
def get_test():
    checked_roles = json.loads(request.args.get('roles'))
    checked_sprints = json.loads(request.args.get('sprints'))
    # checked_sprints.append(1)
    print(checked_roles)
    classes = sqlsession.query(ClassVN) \
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

    class_relationships = sqlsession.query(RelationShipVN) \
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# redirect the user to the uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

# a route for clustering
# @app.route('/clusters')
# def cluster():
#     # get all the nodes that are connected to a role
#     x = 1
#     start_at_role = sqlsession.query(UserStoryVN.functional_role).distinct()
#     list_of_roles = [role.functional_role for role in start_at_role]
#     nodes = []
#     for role in list_of_roles:
#         classes = sqlsession.query(ClassVN) \
#             .join(us_class_association_table) \
#             .join(UserStoryVN) \
#             .filter(or_(UserStoryVN.functional_role == func.lower(role),
#                         UserStoryVN.functional_role == role)) \
#             .all()
#
#         for concept in classes:
#             concept.cluster = x
#             nodes.append([{"name": concept.class_name} for concept in classes])
#         sqlsession.commit()
#         x = x + 1
#
#     json_nodes = json.dumps(nodes)
#
#     return jsonify(roles=list_of_roles, nodes=nodes)


# a route for delivering the list of concepts to be made into nodes
@app.route('/concepts')
def concepts():
    # first apply the "Role" mark to each concept that is a functional_role:
    all_roles = sqlsession.query(ClassVN).filter(ClassVN.group == '1').all()
    # update their "group" attribute
    for role in all_roles:
        role.group = "Role"
        sqlsession.commit()
    # now jsonify and return the concepts to the fore-end
    concepts_query = select([ClassVN])
    concept_list = []
    concepts_query_res = conn.execute(concepts_query)
    for c in concepts_query_res:
        weight2 = 15 + (4 * math.sqrt(c.weight))
        concept_dictionary = {'id': c.class_id, 'label': c.class_name, 'weight': c.weight, 'size': weight2,
                              'group': c.group, 'title': "", 'cid': c.cluster}

        concept_list.append(concept_dictionary)

    json_concepts = json.dumps(concept_list)
    return json_concepts


@app.route('/relationships')
def relationships():
    concepts_query = select([ClassVN])
    relationships_query = select([RelationShipVN])
    relationships_query_result = conn.execute(relationships_query)
    concepts_query_result = conn.execute(concepts_query)
    edges_id_list = []
    concepts_dict = {}
    concepts_dict_list = []
    relationshipslist = []

    for concept in concepts_query_result:
        concepts_dict[concept.class_id] = concept.class_name
        concepts_dict_list.append([concept.class_id, concept.class_name])

    # check if a domain(from) or range(to) is part of the userstory concepts and if so make
    # the relationship between the concepts involved
    for rel in relationships_query_result:
        relationshipslist.append([rel.relationship_domain, rel.relationship_range,
                                  rel.relationship_name, rel.relationship_id])

        # for rel in relationships_query_result:
        for concept in concepts_dict_list:
            if rel.relationship_domain == concept[1]:
                x = concept[0]
        # for rel in relationships_query_result:
        for concept in concepts_dict_list:
            if rel.relationship_range == concept[1]:
                y = concept[0]
        # for rel in relationships_query_result:
        #     for key, value in concepts_dict.items():
        #         if rel.relationship_range == value:
        #             y = key
        #
        # for key, value in concepts_dict.items():
        #     if value == rel.relationship_domain:
        #         x = key
        # for key, value in concepts_dict.items():
        #     if value == rel.relationship_range:
        #         y = key

        edges_id_dict = {'id': rel.relationship_id, 'from': x, 'to': y, 'label': rel.relationship_name}
        # ELSE??
        edges_id_list.append(edges_id_dict)

    json_edges = json.dumps(edges_id_list)

    return json_edges


if __name__ == '__main__':
    app.run()
