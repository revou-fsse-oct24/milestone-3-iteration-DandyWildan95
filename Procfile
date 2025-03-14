release: PYTHONPATH=. flask db upgrade
release: pip install -e . && flask db upgrade
web: gunicorn wsgi:app
