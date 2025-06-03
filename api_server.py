from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
from flask_swagger_ui import get_swaggerui_blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# API Key Configuration
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

def require_api_key(f):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/todos', methods=['GET'])
@require_api_key
def get_todos():
    todos = Todo.query.all()
    return jsonify([{
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    } for todo in todos])

@app.route('/todos', methods=['POST'])
@require_api_key
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False)
    )
    db.session.add(todo)
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    }), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
@require_api_key
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    })

@app.route('/todos/<int:todo_id>', methods=['PUT'])
@require_api_key
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.completed = data.get('completed', todo.completed)
    
    db.session.commit()
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    })

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@require_api_key
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

# Configure Swagger UI
SWAGGER_URL = '/api/docs'  # URL for accessing Swagger UI
API_URL = '/api/openapi.yaml'  # URL for the OpenAPI specification

# Create Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo API"
    }
)

# Register Swagger UI blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve OpenAPI specification
@app.route('/api/openapi.yaml')
def openapi_spec():
    with open('openapi.yaml', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True)