from flask import Flask
from flask_migrate import Migrate
from flask_script import Manager  # Make sure this is installed
from src.app import create_app
from src.models.user import db

application = create_app()
migrate = Migrate(application, db)
manager = Manager(application)  # Use application instead of app

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()