# gunicorn_config.py
workers = 4  # Adjust the number of workers based on your server's resources
bind = "0.0.0.0:8000"  # Host and port where Gunicorn will listen

#gunicorn -c gunicorn_config.py app:app
