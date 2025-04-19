from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from.index import index_views
from.dashboard import dashboard_views
from App.models import User

from App.controllers import (
    login,
    create_user  # Import the create_user function
)
from App.database import db  # Import the db object

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    



@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    response = redirect(request.referrer)
    if not token:
        flash('Bad username or password given'), 401
    else:
        flash('Login Successful')
        response = redirect(url_for('dashboard_views.dashboard_page'))
        set_access_cookies(response, token) 
    return response

@auth_views.route('/signup', methods=['POST'])
def signin_action():
    data = request.form
    existing_user = User.query.filter_by(username=data['username']).first()

    if existing_user:
        flash('⚠️ Username already exists. Please choose a different one.', 'error')
        return redirect(url_for('signup_views.signup_page'))
    newuser = create_user(data['username'], data['password'])
    response = None
    try:
        db.session.add(newuser)
        db.session.commit()
        token = login(data['username'], data['password'])
        response = redirect(url_for('dashboard_views.dashboard_page'))
        set_access_cookies(response, token)
        flash('Account Created!') 
    except Exception:
        db.session.rollback()
        flash('username or email already exists')
        response = redirect(url_for('index_views.index_page'))
    return response




@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.index_page')) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response