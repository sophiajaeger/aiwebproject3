#!/usr/bin/env python3
import sys, os

# Set the project directory (adjust this path if necessary)
project_home = os.path.abspath(os.path.dirname(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables if needed (for example, to set Flask to production)
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app from channel.py and expose it as 'application'
from channel import app as application
