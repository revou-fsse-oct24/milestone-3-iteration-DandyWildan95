from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from src.app import create_app
from src.models.user import db

# Create app and initialize extensions
application = create_app()
migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()