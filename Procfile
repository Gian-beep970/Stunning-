web: gunicorn -w 4 -b 0.0.0.0:$PORT run:app
worker: python run.py
release: python run.py init_db
