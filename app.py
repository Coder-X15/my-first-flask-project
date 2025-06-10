from flask import Flask, render_template, url_for, request, redirect # Import main stuff from Flask for rendering templates and generating URLs
from flask_sqlalchemy import SQLAlchemy # Import Flask-SQLAlchemy library for dealing with databases
from datetime import datetime, timezone

app = Flask(__name__) # a reference to the current file as a Flask app (I mean, the name of the Flask app is this filename)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # for using SQLite database in the relative path ('////' is absolute path)
db = SQLAlchemy(app)

# NB: to create the database, open up a Python shell in this environment and run:
#   from app import app, db
#   with app.app_context():
#       db.create_all()
# The database will be created in  folder 'instance', so update the app.config line accordingly

# defining a class for the database table
class Todo(db.Model):
    # database table to hold the items in the todo list
    id = db.Column(db.Integer, primary_key=True) # the task ID (as a primary key in the database)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now(timezone.utc)) # replacement for the depricated datetime.utcnow() method

    def __repr__(self):
        return '<Task %r>'%(self.id)

@app.route('/', methods = ['POST', 'GET']) # specifying the main route for the webapp
def index():
    # something like index.html
    # return "Hello world!" # - simple return
    if request.method == 'POST':
        task_content = request.form['content']
        date_of_creation = datetime.now(timezone.utc)
        new_task = Todo(content = task_content, date_created = date_of_creation)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Failed to add new task (Reason:{e})"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks= tasks) # renders and returns a template
    
@app.route("/delete/<int:id>")
def delete_task(id):
    # delete a task entry from the database table
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Error deleting the task."

@app.route("/update/<int:id>", methods = ['POST', 'GET'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    # delete a task entry from the database table
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit() # no other actions are needed since we're just updating an existing object
            return redirect('/')
        except:
            return "Error updating task."
    else:
        return render_template('update.html', task=task)
    

if __name__ == "__main__":
    app.run(debug=True) # run the Flask app in debug mode