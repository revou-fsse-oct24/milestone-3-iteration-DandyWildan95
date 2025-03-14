from setuptools import setup, find_packages

setup(
    name='revobank-api',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restful',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-jwt-extended',
        'flask-bcrypt',
        'flask-marshmallow',
        'psycopg2-binary',
        'python-dotenv',
        'marshmallow-sqlalchemy',
        'blinker'
    ],
    entry_points={
        'console_scripts': [
            'revobank=src.app:create_app',
        ],
    },
)