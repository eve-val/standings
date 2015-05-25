from binascii import unhexlify
from hashlib import sha256
from datetime import datetime

from braveapi.client import API
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import NIST256p

from flask import render_template, flash, redirect, url_for, abort, request, jsonify, session, g
from app import app, coreapi, db, models
from .forms import ConfirmStanding, SearchStanding
from .coreapi import CoreAPI, CoreSession

import cgi


CHECK_LOGIN_EXCLUDE_ENDPOINTS = ['authorize', 'authorized']
@app.before_request
def check_login():
    if request.endpoint not in CHECK_LOGIN_EXCLUDE_ENDPOINTS:
        if 'token' in session:
            core_session = coreapi.get_session(session['token'])
            # TODO: check perms here
            g.core_session = core_session
            g.user = core_session.get_user()
        else:
            return redirect('/authorize')

@app.route('/session_info')
def session_info():
    if g.core_session:
        return jsonify(g.core_session.info)
    return "No active session"

@app.route('/perm_info')
def perm_info():
    return "View: {0}<br/>Edit: {1}<br/>core.application.create: {2}" \
        .format(g.core_session.has_view_perm(), g.core_session.has_edit_perm(), g.core_session.has_perm('core.application.create'))


@app.route('/')
@app.route('/standings')
def index():
    standings = models.Standing.query.all()
    
    return render_template("standings.html",
                           title='Standings',
                           user=g.user,
                           standings=standings)

@app.route('/add_standing', methods=['GET', 'POST'])
def add_standing():
    
    form = SearchStanding()
    if form.validate_on_submit():
        
        if form.entity_type.data == 'alliance':
            flash('alliance')
        else:
            flash('corp')
        preview_form = ConfirmStanding()
        return render_template('standing_add_preview.html',
                               form = preview_form,
                               entity_type = form.entity_type.data,
                               standing = form.standing.data,
                               entity_id = 'id',
                               corporation_name = 'corp name',
                               corporation_ticker = 'corp ticker',
                               alliance_name = 'alliance name',
                               alliance_ticker = 'alliance ticker')
    if form.errors:
        for field_name, field_errors in form.errors.items():
            flash(u"Error in %s: %s" % (form[field_name].label.text, "<br>".join(field_errors)))
    return render_template('standing_add_search.html', 
                           title='Add Standing',
                           form=form)
                           

@app.route('/do_edit_standing', methods=['GET', 'POST'])
def do_edit_standing():
    form = ConfirmStanding()
    if form.validate_on_submit():
        if form.entity_type == 'alliance':
            flash('alliance')
            models.Standing.query.filter_by()
        else:
            flash('corp')
        
        
    if form.errors:
        for field_name, field_errors in form.errors.items():
            flash(u"Error in %s: %s" % (form[field_name].label.text, "<br>".join(field_errors)))
    return redirect('/add_standing')

# Perform the initial API call and direct the user.
@app.route('/authorize')
def authorize():
    api = coreapi.get_api()

    # Build Success/Failure Redirect URLs
    success = str("http://"+app.config['SERVER_NAME']+url_for('authorized'))
    failure = str("http://"+app.config['SERVER_NAME']+url_for('fail'))

    # Make the authentication call to the CORE Service
    result = api.core.authorize(success=success, failure=failure)
    
    print result.__repr__()

    if 'location' in result:
        # Redirect based on the authentication request validity
        return redirect(result.location)
    else:
        return 'Error authorizing app: {0}'.format(result.message)


# Root URI
@app.route('/authorized')
def authorized():
    # Perform the initial API call and direct the user.

    api = coreapi.get_api()

    # Build Success/Failure Redirect URLs
    token = request.args.get('token', '')

    if not token:
        abort(401)

    session['token'] = token

    return redirect('/session_info')


# Root URI
@app.route('/fail')
def fail():
    abort(401)

@app.route('/logout')
@app.route('/ciao')
def logout():
    session.pop('token', None)
    return "Logged out"

@app.route('/posts')
def posts():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)
