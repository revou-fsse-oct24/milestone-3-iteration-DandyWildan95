web: gunicorn 
"src.app:create_app()"
release: PYTHONPATH=. flask --app src.app db upgrade