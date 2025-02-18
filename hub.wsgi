import sys
import os
import site

# Add your project directory so Python can find your modules (e.g. hub.py)
sys.path.insert(0, "/home/u006/aiwebproject3")

# Add the virtual environment's site-packages directory to the Python path.
venv_site = "/home/u006/venv/lib/python3.10/site-packages"
site.addsitedir(venv_site)

# Now import your app from hub.py
from hub import app

# Set the WSGI application callable for Apache
application = app


