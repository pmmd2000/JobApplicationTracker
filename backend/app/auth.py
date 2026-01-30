from flask import Blueprint, url_for, session, redirect, jsonify, current_app, request
from .extensions import oauth
from .models import User
from .database import db

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

def get_google_client():
    client = oauth.create_client('google')
    if not client:
        oauth.register(
            name='google',
            client_id=current_app.config['GOOGLE_CLIENT_ID'],
            client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'},
        )
        client = oauth.create_client('google')
    return client

@auth.route('/login')
def login():
    google = get_google_client()
    redirect_uri = url_for('auth.callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth.route('/callback')
def callback():
    google = get_google_client()
    try:
        token = google.authorize_access_token()
        user_info = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
        
        google_id = user_info.get('sub') or user_info.get('id')
        if not google_id:
            raise ValueError("No user ID found in Google response")
        
        # Upsert user
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            user = User(
                google_id=google_id,
                email=user_info['email'],
                name=user_info.get('name', ''),
                avatar_url=user_info.get('picture', '')
            )
            db.session.add(user)
        else:
            # Update info
            user.name = user_info.get('name', user.name)
            user.avatar_url = user_info.get('picture', user.avatar_url)
        
        db.session.commit()
        
        # Set session
        session['user_id'] = user.id
        
        # Redirect to frontend dashboard
        return redirect('/') 
    except Exception as e:
        current_app.logger.error(f"Auth failed: {str(e)}")
        return jsonify({'error': 'Authentication failed', 'details': str(e)}), 400

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})

@auth.route('/me')
def me():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'authenticated': False}), 200
        
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return jsonify({'authenticated': False}), 200
        
    return jsonify({
        'authenticated': True,
        'user': user.to_dict()
    })
