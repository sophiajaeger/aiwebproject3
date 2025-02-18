import sys
import os
import site
from dotenv import load_dotenv

# Add your project directory so Python can find your modules (e.g. hub.py)
sys.path.insert(0, "/home/u006/aiwebproject3")

# Add the virtual environment's site-packages directory to the Python path.
venv_site = "/home/u006/venv/lib/python3.10/site-packages"
site.addsitedir(venv_site)

# Load environment variables from a secure .env file outside the public directory
load_dotenv("/home/u006/.env")

# Now import your app
from hub import app

application = app


