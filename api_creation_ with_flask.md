# Creation of the Shopping List API with Flask

## Project Setup
1. Create a project folder.
2. Create a virtual environment:
   - Windows: `python -m venv {name_of_environment}`
   - Mac/Linux: `python3 -m venv {name_of_environment}`
3. Activate the virtual environment:
   - Windows: `{name_of_environment}\Scripts\activate`
   - Mac/Linux: `source {name_of_environment}/bin/activate`
4. Install Flask module: `pip install flask`.

## Flask App Setup
1. Create an instance of the Flask class.
- create folder called 'app' in your main directory.
- create file '__init__.py'.
    - have the following code in here initially:
        ```
        from flask import Flask
        
        app = Flask(__name__)
        
        from . import routes
        ```

## Initial Routes
1. Create a file named 'routes.py' in the folder 'app'.  
    import the following:
    ```
    from app import app
    from shopping_list import shopping_list
    ##ensure the 'shopping_list.py' file is in the root dir of app (next to the `app` folder)
    ```  
    Add an index route in the file so that you may see something on the landing page when you run the live server with `flask --debug run` and follow link to the local server.  
    ```
    @app.route('/')
    def index():
        return 'Hello There! Welcome to the Shopping List API!'
    ```  
    If set up correctly so far, going to the live dev server will display the contents of `shopping_list.py` as a json dictionary.  

2. In `routes.py`, continue to add the initial routes such as:  
    - [GET] All ingredients - Return all tasks in the `shopping_list`.
    - [GET] Single ingredient by ID
    - [POST] Add a new ingredient. ensure to include parameters for required fields.

## Saving/Installing PIP Dependencies

1. Save the dependencies to a `requirements.txt` file with command:  
    `pip freeze > requirements.txt`
This will save all the dependencies to a file that can be used to install the dependencies in another environment.  

2. Dependencies can be installed in another environment with the command:  
    `pip install -r requirements.txt`

## Initial Database Setup

1. Install Flask-SQLAlchemy and Flask-Migrate:  
    `pip install flask-sqlalchemy flask-migrate`


2. Set up a `config.py` file in the root directory. Add the following to contents:  
    ```
    import os

    basedir = os.path.abspath(os.path.dirname(__file__))

    class Config:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    ```
    You can also enter a `key = value` pair in a `.env` file in the root directory to store the database URI if you'd like to connect to an external database.  
    Here's a sample `.env` file:

    ```
    key = value

    DATABASE_URL = `postgresql://username:password@localhost/db_name`
    ```
    Ensure to add the `.env` file to the `.gitignore` file to prevent it from being pushed to the repository. If you're using a `.env` file, also run command `pip install python-dotenv` to ensure the app can read the file. 
<br>

3. Create `models.py` with all the columns for the tables with the attributes, such as:
    ```
    from . import db
    from datetime import datetime, timezone
    
    class Ingredient(db.Model):
        ingredient_id = db.Column(db.Integer, primary_key=True)
        ingredient = db.Column(db.String, nullable=False)
        description = db.Column(db.String, nullable=False)
        status = db.Column(db.Boolean, nullable=False, default=False)
        date_added = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    ```
4. Add SQLAlchemy & Migrate to the `__init__.py` to ensure the app is aware of the database and migrations.  
    Also ensure to add `models` here as well.  
    ```
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from config import Config
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    from . import routes, models
    ```
5. Initialize migrations folder: 
    `flask db init`
6. Create the first migration: 
    `flask db migrate -m "YOUR MESSAGE HERE"`
7. Apply the migration: 
    `flask db upgrade`

## Database Integration
1. Update routes to interact with the database:
   - [GET] `/tasks` - Retrieve all tasks from the database.
   - [GET] `/tasks/<task_id>` - Retrieve task by ID.
   - [POST] `/tasks` - Add a task to the database.

## Optional Challenge
1. Add a query parameter to filter completed or incomplete tasks in `/tasks` route.

## Complete Task API
1. Implement CRUD operations for tasks:
   - [PUT] `/tasks/<task_id>` - Update a task.
   - [DELETE] `/tasks/<task_id>` - Delete a task.
2. Implement user authentication and user-related routes:
   - [POST] `/users` - Create a new user.
   - [GET] `/users/<user_id>` - Get user by ID.
   - [PUT] `/users/<user_id>` - Update user.
   - [DELETE] `/users/<user_id>` - Delete user.
   - [GET] `/token` - Get a token based on username and password.
   - [GET] `/me` - Return authenticated user with tasks (bonus).

## HTML Root Document
1. Create a `templates` folder inside the `app` folder.
2. Inside the `templates` folder, create an `index.html` file with your desired content.  
    a. This can be used to host instructions for using/accessing the API.

## Hosting
1. Host your application on Render.

## Submission
- Commit the project to GitHub.
- Submit the GitHub link for the assignment.
