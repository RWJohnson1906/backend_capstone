from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os 

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def __init__(self, title):
        self.title = title

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Add Endpoint
@app.route('/api/tasks', methods=['POST'])
def add_task():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    post_data = request.get_json()
    title = post_data.get('title')
    new_task = Task(title)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(task_schema.dump(new_task))

# Get Endpoint
@app.route('/api/get/tasks', methods=['GET'])
def get_tasks():
    all_tasks = db.session.query(Task).all()
    return jsonify(tasks_schema.dump(all_tasks))

# Put Endpoint
@app.route('/api/edit/tasks/<id>', methods=['PUT'])
def edit_task_id(id):
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be sent as JSON")
    
    put_data = request.get_json()
    title = put_data.get('title')

    edit_task_id = db.session.query(Task).filter(Task.id == id).first()

    if title != None:
        edit_task_id.title = title

        db.session.commit()

    return jsonify(task_schema.dump(edit_task_id))

# Delete Endpoint
@app.route('/api/delete/task/<id>', methods=["DELETE"])
def delete_task_id(id):
    delete_task_id = db.session.query(Task).filter(Task.id == id).first()
    db.session.delete(delete_task_id)
    db.session.commit()

    return jsonify("Task has been deleted", task_schema.dump(delete_task_id))




if __name__ == '__main__':
    app.run(debug=True)
