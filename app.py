from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, JournalEntry
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'})
    
    # Auth routes
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')
            
            if not email or not password:
                return jsonify({'error': 'Email and password are required'}), 400
            
            if User.query.filter_by(email=email).first():
                return jsonify({'error': 'User already exists'}), 409
            
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password, name=name)
            
            db.session.add(new_user)
            db.session.commit()
            
            access_token = create_access_token(identity=str(new_user.id))
            
            return jsonify({
                'message': 'User created successfully',
                'access_token': access_token,
                'user': {'id': new_user.id, 'email': new_user.email, 'name': new_user.name}
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Journal routes
    @app.route('/api/journal/entries', methods=['POST'])
    @jwt_required()
    def create_journal_entry():
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            content = data.get('content')
            emotion = data.get('emotion')
            
            if not content:
                return jsonify({'error': 'Content is required'}), 400
            
            # Simple sentiment analysis
            sentiment = 'neutral'
            score = 50
            
            new_entry = JournalEntry(
                user_id=user_id,
                content=content,
                sentiment=sentiment,
                score=score,
                emotion=emotion
            )
            
            db.session.add(new_entry)
            db.session.commit()
            
            return jsonify({
                'message': 'Journal entry created successfully',
                'entry': {
                    'id': new_entry.id,
                    'content': new_entry.content,
                    'sentiment': new_entry.sentiment,
                    'score': new_entry.score,
                    'emotion': new_entry.emotion
                }
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    print('Starting Mood Journal Backend...')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
