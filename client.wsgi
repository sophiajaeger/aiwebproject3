import sys
import os

# Ensure the current directory is in the sys.path
sys.path.insert(0, os.path.dirname(__file__))

from client import app as application
