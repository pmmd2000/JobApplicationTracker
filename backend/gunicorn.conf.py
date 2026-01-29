# Gunicorn configuration file

bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
accesslog = "-"
errorlog = "-"
loglevel = "info"
