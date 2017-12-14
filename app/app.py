#!/usr/bin/env python
import sys
import os
import math
import json
import datetime

sys.path.append('/var/www/interactivenarrator')

from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, not_, or_
from flask import Flask, jsonify, render_template, url_for, request
from flask import flash, send_from_directory, Response, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug import secure_filename, redirect
from passlib.hash import sha256_crypt
from form import SetInfoForm, LoginForm, RegistrationForm, ContactForm
from post import add_data_to_db
import config
sys.path.append('/var/www/VisualNarrator')

from VisualNarrator import run

# preload Spacey NLP
spacy_nlp = run.initialize_nlp()

# import the database models
from models import Base, User, UserStoryVN, RelationShipVN, ClassVN, CompanyVN, \
    SprintVN, engine, us_class_association_table, \
    us_relationship_association_table, \
    us_sprint_association_table


# configuration settings from config.py
app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.Model = Base

mail = Mail()
mail.init_app(app)
# NOTE: sqlsession vs session usage: session is a login/logout browser session while sqlsession is a Session() object

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sqlsession = Session()
conn = engine.connect()


# FLASK SECURITY

# from flask_security import Security, login_required,\
#     SQLAlchemySessionUserDatastore
# from flask_login import LoginManager, UserMixin
# from models import User, Role
#
# login_manager = LoginManager()
# login_manager.init_app(app)
#
# # user_datastore = SQLAlchemySessionUserDatastore(sqlsession, User, Role)
#
# @app.before_first_request
# def create_user():
#     # init_db()
#     # user_datastore.create_user(email='govertjan@msn.com', password='qwerty')
#     sqlsession.commit()
#
# # Views
# @app.route('/flasksec')
# @login_required
# def flask_sec():
#     return render_template('index.html')
# END FLASK SECURITY

# route for the demopage. Not accessible to users that are logged in
@app.route('/demo', methods=['GET', 'POST'])
def demo():
    session['logged_in'] = False
    session['username'] = ''

    if session['logged_in']:
            # or session['username'] !='demoman':
        return redirect(url_for('homepage'))

    else:
        username = 'demoman'
        # session['logged_in'] = True
        session['username'] = username
        return render_template('visdemo.html')


# route for reaching the homepage
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('ERROR POSTING FORM')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender=app.config['MAIL_USERNAME'], recipients=['interactivenarratoruu@gmail.com'])
            msg.body = """
              From: %s <%s>
              %s
              """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            print('form was sent to server')
            return render_template('contact.html', form=form, success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)

# route for displaying the visualization
@app.route('/vis', methods=['GET', 'POST'])
def show_vis():
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
            print('validating was a success')
            username = form.username.data
            company_name = form.company_name.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            # check if a user is new or existent...
            user_exists = sqlsession.query(User).filter(User.username == username).first()
            # ... if it exists, notify the user
            if user_exists:
                error = "That username is already taken, please choose another"
                return render_template('register.html', form=form, error=error)
            # ..else, create the new user and company
            else:
                print('success, user does not exist yet')
                sqlsession.add(CompanyVN(company_name=company_name))
                the_company = sqlsession.query(CompanyVN).order_by(CompanyVN.id.desc()).first()
                new_user = User(username=username, company_name=company_name, email=email, password=password,
                                company_id=the_company.id)
                sqlsession.add(new_user)

                sqlsession.commit()
                # flash('thanks for registering')

                session['logged_in'] = True
                session['username'] = username

                if session['username'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('show_dash'))

        else:
            return render_template("register.html", form=form)

    except Exception as e:
        print('an exception occured', e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        sqlsession.rollback()

        error = 'Sorry, we could not register you'

        return render_template('register.html', form=form, error=error)


# route for when the login form on the homepage is submitted
@app.route('/login', methods=['GET', 'POST'])
def do_login():
    form = LoginForm(request.form)
    if not session.get('logged_in'):
        if request.method == "POST":
            try:

                POST_USERNAME = str(request.form['username'])
                POST_PASSWORD = str(request.form['password'])

                # check if a user with the entered username exists
                check_user = sqlsession.query(User).filter(User.username.in_([POST_USERNAME]))

                user_exists = check_user.first()
                # print(user_exists.password)
                if user_exists:
                    # flash('Wrong username/password, please try again')
                    # if the password matches the username, log the user in
                    if sha256_crypt.verify(POST_PASSWORD, user_exists.password):
                        print(user_exists)
                        # set the username in the session to the username that was just logged in
                        session['username'] = POST_USERNAME
                        session['logged_in'] = True
                        flash('Thanks for logging in!')
                        print('login succes')
                        user_exists.last_login_at = datetime.datetime.utcnow()
                        if user_exists.login_count == None:
                            user_exists.login_count = 0
                        user_exists.login_count = user_exists.login_count + 1

                        sqlsession.commit()

                        if session['username'] == 'admin':
                            return redirect(url_for('admin_dashboard'))
                        else:
                            return redirect(url_for('show_dash'))
                    else:
                        error = 'Could not login. Wrong password/username?'
                        print('failure on login')
                        return render_template('login.html', form=form, error=error)
                else:
                    error = 'Sorry, wrong password/username'
                    return render_template('login.html', form=form, error=error)

            except Exception as e:
                print('Exception raised on login', e)

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                error = 'Sorry, there was an unexpected error'
                return render_template('login.html', form=form, error=error)

        else:
            return render_template('login.html', form=form)

    else:
        return redirect(url_for('show_dash'))

# route for logging out the user. This resets the username to empty and status to not logged in
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ''
    return redirect(url_for('homepage'))

# admin page
@app.route("/admindashboard")
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('do_login'))
    if session['username'] == 'demoman':
        return redirect(url_for("demo"))
    if session.get('logged_in') and session['username'] == 'admin':
        sprints = []
        username = session['username']
        print(username)
        # show all the sprints that are in the database on the dashboard page
        all_sprints = sqlsession.query(SprintVN)\
            .join(CompanyVN)\
            .join(User).filter(User.username == username).all()

        for sprint in all_sprints:
            user_story_count = sqlsession.query(UserStoryVN).filter(UserStoryVN.in_sprint == sprint.id).count()
            print('COUNT USER STORIES', user_story_count)
            sprint = dict(sprint_id=sprint.id,
                          sprint_id_user = sprint.sprint_id_user,
                        sprint_name=sprint.sprint_name,
                        company_id=sprint.company_id,
                        company_name=sprint.company_name,
                        user_story_count = user_story_count)
            sprints.append(sprint)

        registered_users = sqlsession.query(User).all()

        # check what company name is regeistered for this user
        company_present = sqlsession.query(CompanyVN).join(User).filter(User.username == username).first()

        if company_present:
            company_name = company_present.company_name
        else:
            company_name = ''

        return render_template("admindashboard.html", sprints=sprints, username=username, company_name=company_name, registered_users=registered_users)

    return redirect(url_for('do_login'))

# route for reaching the dashboard page for logged in users
@app.route("/dashboard")
def show_dash():
    if not session.get('logged_in'):
        return redirect(url_for('do_login'))
    # if session['username'] == 'demoman':
    #     return redirect(url_for("demo"))
    if session.get('logged_in') and session['username'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        sprints = []
        username = session['username']
        print(username)
        # show all the sprints that are in the database on the dashboard page
        all_sprints = sqlsession.query(SprintVN)\
            .join(CompanyVN)\
            .join(User).filter(User.username == username).all()

        for sprint in all_sprints:
            user_story_count = sqlsession.query(UserStoryVN).filter(UserStoryVN.in_sprint == sprint.id).count()
            print('COUNT USER STORIES', user_story_count)
            sprint = dict(sprint_id=sprint.id,
                          sprint_id_user = sprint.sprint_id_user,
                        sprint_name=sprint.sprint_name,
                        company_id=sprint.company_id,
                        company_name=sprint.company_name,
                        user_story_count = user_story_count)
            sprints.append(sprint)

        # extra data for admin
        if username == 'govertjan':
            registered_users = sqlsession.query(User).all()
        else:
            registered_users = ''
        # check what company name is regeistered for this user
        company_present = sqlsession.query(CompanyVN).join(User).filter(User.username == username).first()

        if company_present:
            company_name = company_present.company_name
        else:
            company_name = ''

        return render_template("dashboard.html", sprints=sprints, username=username, company_name=company_name, registered_users=registered_users)


# View for clearing all sets for a particular user
@app.route("/delete_all")
def delete_all():
    # get all userstories and delete them one by one
    # the cascade makes sure all sprints, relationships, classes and association table entries are deleted as well

    active_user = sqlsession.query(User).filter(User.username == session['username']).first()

    # find and delete all user stories and the classes, relationships connected to them
    userstories = sqlsession.query(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN).filter(SprintVN.user_id == active_user.id) \
        .join(CompanyVN) \
        .join(User).filter(User.username == active_user.username).all()


    for userstory in userstories:
        sqlsession.delete(userstory)
        # sqlsession.commit()

    # find orphan sprints and delete them if necessary
    sprints = sqlsession.query(SprintVN).filter(SprintVN.user_id == active_user.id).all()

    for sprint in sprints:
        sqlsession.delete(sprint)

    try:
        sqlsession.commit()
        return redirect(url_for('show_dash'))
    except Exception as e:
        print('Exception raised', e)

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        sqlsession.rollback()
        return redirect(url_for('show_dash'))



@app.route('/delete_sprint/<int:id>', methods=['GET', 'POST'])
def delete_sprint(id):
    active_user = sqlsession.query(User).filter(User.username == session['username']).first()

    userstories = sqlsession.query(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .join(CompanyVN) \
        .join(User).filter(and_(SprintVN.id == id), (User.username == active_user.username)).all()

    for userstory in userstories:
        sqlsession.delete(userstory)

    try:
        sqlsession.commit()
        return redirect(url_for('show_dash'))

    except Exception as e:
        print('Exception raised', e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        sqlsession.rollback()
        return redirect(url_for('show_dash'))


# route for the form that enables uploading of files containing user stories
@app.route('/uploadform', methods=['GET', 'POST'])
def upload_form():
    if session.get('logged_in'):
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

        if request.method == 'POST' and form.validate():
            sprint_form_data = {}
            # sprint_form_data['sprint_id'] = form.sprint_id.data
            sprint_form_data['sprint_name'] = form.sprint_name.data
            # check of the inserted sprint values already exist
            sprint_exists = sqlsession.query(SprintVN).filter\
                (SprintVN.sprint_name == sprint_form_data['sprint_name'])\
                .join(CompanyVN)\
                .join(User).filter(User.username == active_user.username)\
                .first()
            #check if the user already has sprints, regardless of their name, and apply a user speficic id to it
            newest_user_sprint = sqlsession.query(SprintVN).order_by(SprintVN.sprint_id_user.desc())\
                .join(CompanyVN)\
                .join(User).filter(User.username == active_user.username)\
                .first()
            if newest_user_sprint:
                highest_user_sprint_id = newest_user_sprint.sprint_id_user
            else:
                highest_user_sprint_id = 0

                # if the sprint already exists, notify the user...
            if sprint_exists:
                error = 'This sprint name is already in the database. Please choose a different name'
                print('sprint exists already', sprint_exists)
                return render_template('uploadform.html', form=form, error=error)
            # ...if it doesn't, add it to the DB
            else:
                # FILE UPLOAD HANDLING
                file = request.files['file']
                if file.filename == '':
                    error = 'No file was selected for uploading'
                    return render_template('uploadform.html', form=form, error=error)
                # Check if the file is one of the allowed types/extensions
                if file and allowed_file(file.filename):
                    # Make the filename safe, remove unsupported chars and spaces
                    filename = secure_filename(file.filename)
                    # Move the file form the temporal folder to...
                    # ...the upload folder we setup
                    print('SECURE FILENAME', filename)

                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    # set the filename so Visual Narrator can handle it
                    set_filename = 'uploads/' + filename


                    try:
                        sqlsession.add(SprintVN(sprint_id_user=highest_user_sprint_id + 1, sprint_name=sprint_form_data['sprint_name'],
                                                company_name=active_company_name, company_id=active_company.id, user_id=active_user.id))
                        print('added sprint')
                        # now add the sprint to the database
                        sqlsession.commit()
                        # find the sprint that was just added,
                        newest_sprint = sqlsession.query(SprintVN).filter(and_(
                            SprintVN.sprint_name == sprint_form_data['sprint_name']), (SprintVN.user_id == active_user.id)) \
                            .order_by(SprintVN.id.desc())\
                            .first()

                        # and obtain its ID
                        sprint_form_data['sprint_id'] = newest_sprint.id

                        # run the visual narrator back-end and obtain needed objects for visualization
                        data = run.call(set_filename, spacy_nlp)
                        #  run the poster.add_data_to_db method to place the objects and their attributes in the database
                        add_data_to_db(data['us_instances'], data['output_ontobj'], data['output_prologobj'], data['matrix'],
                                       sprint_form_data)
                    except UnicodeDecodeError:
                        error = 'Sorry, the file was not accepted by our system. ' \
                                'It might be ASCII encoded, Please try UTF-8 Unicode encoding for your file'
                        if newest_sprint:
                            sqlsession.delete(newest_sprint)
                            sqlsession.commit()
                        else:
                            pass
                        return render_template('uploadform.html', form=form, error=error)

                    except TypeError:
                        error = 'Sorry, datatype of the file was not accepted by our system. ' \
                                'Please try UTF-8 UNICODE in .txt or .csv files'
                        if newest_sprint:
                            sqlsession.delete(newest_sprint)
                            sqlsession.commit()
                        else:
                            pass
                        return render_template('uploadform.html', form=form, error=error)


                    except IndexError:
                        error = 'Sorry, the file was not accepted by our system. ' \
                                'Does it really contain user stories in the format "as a (role) I want to (goal)"?'
                        if newest_sprint:
                            # sqlsession.query(SprintVN).filter(SprintVN.sprint_name == newest_sprint.sprint_name).delete()
                            sqlsession.delete(newest_sprint)
                            sqlsession.commit()
                            print('the newest sprint is deleted because of content')
                        else:
                            pass
                        return render_template('uploadform.html', form=form, error=error)

                    except Exception as e:
                        print('Exception raised at file processing', e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)

                        if newest_sprint:
                            sqlsession.delete(newest_sprint)
                            sqlsession.commit()
                        else:
                            pass
                        error = 'Sorry, the file could not be processed. ' \
                                'Please try UNICODE in .txt or .csv files'

                        return render_template('uploadform.html', form=form, error=error)


                    # if all went well redirect the user to the visualization directly
                    return redirect(url_for('show_vis'))
                else:
                    error = 'Sorry, the app could not accept and process your file.'

                    newest_sprint = sqlsession.query(SprintVN).filter(and_(
                        SprintVN.sprint_name == sprint_form_data['sprint_name']), (SprintVN.user_id == active_user.id)) \
                        .order_by(SprintVN.id.desc()) \
                        .first()

                    if newest_sprint:
                        sqlsession.delete(newest_sprint)
                        sqlsession.commit()
                    else:
                        pass

                    return render_template('uploadform.html', form=form, error=error)

        else:
            # print('nothing was added to the database')
            return render_template('uploadform.html', form=form)

    else:
        return redirect(url_for('do_login'))

    # return render_template('uploadform.html', form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# get the roles to populate the multiselect with javascript
@app.route('/getroles')
def get_roles():
    username = session['username']

    functional_roles = sqlsession.query(UserStoryVN.functional_role.distinct().label("functional_role"))\
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .join(CompanyVN) \
        .join(User).filter(User.username == username)
    all_roles = [row.functional_role for row in functional_roles.all()]
    print(all_roles)
    return jsonify(all_roles)

# get the sprints to populate the multiselect with javascript
@app.route('/getsprints')
def get_sprints():
    username = session['username']
    # print(username)
    # show all the sprints that are in the database for this user on the dashboard page

    sprints = sqlsession.query(SprintVN) \
        .join(CompanyVN) \
        .join(User).filter(User.username == username).all()

    all_sprints = [[sprint.sprint_name, sprint.sprint_id_user] for sprint in sprints]

    print(all_sprints)
    return jsonify(all_sprints)

# this route displays the userstories to which a node belongs when you click on the node
@app.route('/clickquery')
def click_query():
    clicked_nodes = json.loads(request.args.get('nodes'))
    checked_roles = json.loads(request.args.get('roles'))
    checked_sprints = json.loads(request.args.get('sprints'))

    active_user = sqlsession.query(User).filter(User.username == session['username']).first()

    # find the user_sprint_ids that belong to the sprint_ids
    checked_sprints_ids = sqlsession.query(SprintVN) \
        .filter(and_(SprintVN.user_id == active_user.id),(SprintVN.sprint_id_user.in_(checked_sprints))).all()

    checked_sprints_ids_list = [sprint.id for sprint in checked_sprints_ids]

    print('SELECETD ROLES AND SPRINTS', checked_roles, checked_sprints, checked_sprints_ids, checked_sprints_ids_list)
    node_userstory_list = []
    # active_user = sqlsession.query(User).filter(User.username == session['username']).first()

    for one_node in clicked_nodes:
        print('CLICKED NODE/CONCEPT ID', one_node['id'])
        # node_concept = sqlsession.query(ClassVN).filter(ClassVN.class_id == one_node['id']).all()

        node_userstories = sqlsession.query(UserStoryVN)\
            .join(us_class_association_table)\
            .join(ClassVN) \
            .filter(and_(ClassVN.class_id == one_node['id']),
                    (ClassVN.user == active_user.id)) \
            .filter(and_(UserStoryVN.functional_role.in_(checked_roles),(UserStoryVN.in_sprint.in_(checked_sprints_ids_list))))\
            .all()


        print('THE USER STORIES THAT SHOULD BE PRINTED', node_userstories)

        if node_userstories:
            node_userstory_list = [{"id": us.userstory_id, "text":us.text, "in sprint":us.in_sprint} for us in node_userstories]
        else:
            node_userstory_list = []
        print('ALL THE SELECTED USERSTORIES', node_userstory_list)
    return jsonify(node_userstory_list)


# this is the main query that queries the database for concepts and relationships basd on the
# roles and sprints that were selected by the user.
# This function returns an array of nodes that are
# connected (i.e. occur in a user story where the role occurs in) to the selected role.
@app.route('/query')
def get_nodes_edges():
    # retrieve the sprints and roles to look up, based on the user's selection
    checked_roles = json.loads(request.args.get('roles'))
    checked_sprints = json.loads(request.args.get('sprints'))

    active_user = sqlsession.query(User).filter(User.username == session['username']).first()

    # find the user_sprint_ids that belong to the sprint_ids
    checked_sprints_ids = sqlsession.query(SprintVN) \
        .filter(and_(SprintVN.user_id == active_user.id),(SprintVN.sprint_id_user.in_(checked_sprints))).all()

    checked_sprints_ids_list = [sprint.id for sprint in checked_sprints_ids]

    # retrieve all the classes belonging to the selection
    print('CHECKED ROLES AND SPRINTS @ /QUERY', checked_roles, checked_sprints, checked_sprints_ids_list)
    classes = sqlsession.query(ClassVN) \
        .join(us_class_association_table) \
        .join(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .filter(and_(
        UserStoryVN.functional_role.in_(checked_roles)),
        (SprintVN.id.in_(checked_sprints_ids_list))
    ) \
        .all()
    # put all the classes in a list of dicts
    nodes = [{"label": cl.class_name, "weight": cl.weight, "id": cl.class_id} for cl in classes]
    print('THE NODES ARE HERE', nodes, len(nodes))
    # find all the unique class names
    class_names = [cl.class_name for cl in classes]
    # make a list of all class names and ids
    class_name_id_map = {cl.class_name: cl.class_id for cl in classes}
    print('CLASS_NAME_ID_MAP', len(class_names), len(class_name_id_map))

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
        (SprintVN.id.in_(checked_sprints_ids_list))
    ) \
        .all()
    print('HERE ARE THE RELATIONSHIPS', len(class_relationships), [{"id": rel.relationship_id, "domain": rel.relationship_domain, "range": rel.relationship_range} for rel in class_relationships])
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
            print("Impossible relationship: %s : %s -> %s -> %s" % (class_relationship.relationship_id,
            class_relationship.relationship_domain, class_relationship.relationship_name,
            class_relationship.relationship_range))
            pass


    return jsonify(nodes=nodes, edges=edges)





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

    username = session['username']
    # show all the sprints that are in the database on the dashboard page
    concepts_query = sqlsession.query(ClassVN) \
        .join(us_class_association_table) \
        .join(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .join(CompanyVN)\
        .join(User)\
        .filter(User.username == username)\
        .all()

    # now jsonify and return the concepts to the fore-end
    # concepts_query = sqlsession.query(ClassVN).all()
    concept_list = []
    # concepts_query_res = conn.execute(concepts_query)
    for c in concepts_query:
        weight2 = 15 + (4 * math.sqrt(c.weight))
        concept_dictionary = {'id': c.class_id, 'label': c.class_name, 'weight': c.weight, 'size': weight2,
                              'group': c.group, 'cid': c.cluster}

        concept_list.append(concept_dictionary)

    json_concepts = json.dumps(concept_list)
    return json_concepts


@app.route('/relationships')
def relationships():
    username = session['username']
    # show all the sprints that are in the database on the dashboard page
    concepts_query = sqlsession.query(ClassVN) \
        .join(us_class_association_table) \
        .join(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .join(CompanyVN) \
        .join(User).filter(User.username == username) \
        .all()

    # show all the sprints that are in the database on the dashboard page
    relationships_query = sqlsession.query(RelationShipVN) \
        .join(us_relationship_association_table) \
        .join(UserStoryVN) \
        .join(us_sprint_association_table) \
        .join(SprintVN) \
        .join(CompanyVN) \
        .join(User).filter(User.username == username) \
        .all()

    edges_id_list = []
    concepts_dict = {}
    concepts_dict_list = []
    relationshipslist = []

    for concept in concepts_query:
        concepts_dict[concept.class_id] = concept.class_name
        concepts_dict_list.append([concept.class_id, concept.class_name])

    # check if a domain(from) or range(to) is part of the userstory concepts and if so make
    # the relationship between the concepts involved
    for rel in relationships_query:
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
        if rel.relationship_name == 'isa':
            edges_id_dict = {'id': rel.relationship_id, 'from': x, 'to': y, 'label': rel.relationship_name, 'dashes': "true"}
        else:
            edges_id_dict = {'id': rel.relationship_id, 'from': x, 'to': y, 'label': rel.relationship_name}
        # ELSE??
        edges_id_list.append(edges_id_dict)

    json_edges = json.dumps(edges_id_list)

    return json_edges


# custom error for 500
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('server_error.html'), 500

# custom error for 404
@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('not_found_error.html'), 404


if __name__ == '__main__':
    app.run()
