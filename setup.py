from setuptools import setup, find_packages

setup(
    name='revobank-api',
    version='0.1.0',
    description='RevoBank RESTful API for Banking Services',
    author='RevoBank Development Team',
    author_email='dev@revobank.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'flask>=2.1.0',
        'flask-restful>=0.3.9',
        'flask-sqlalchemy>=2.5.1',
        'PyJWT>=2.3.0',
        'psycopg2-binary>=2.9.3',
        'email-validator>=1.1.3',
        'python-dotenv>=0.19.2',
    ],
    extras_require={
        'dev': [
            'pytest>=7.1.1',
            'coverage>=6.3.2',
            'black>=22.3.0',
            'flake8>=4.0.1',
        ],
        'prod': [
            'gunicorn>=20.1.0',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'revobank-api=src.app:main',
        ],
    },
)