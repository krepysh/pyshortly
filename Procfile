release: flask db upgrade
build: flask db migrate
web: gunicorn -b :$PORT app:app
