import sys
import os

# Add your project directory to sys.path
sys.path.insert(0, "/home/u006/public_html/aiwebproject3")

# Activate your virtual environment
activate_this = os.path.join("/home/u006/public_html/aiwebproject3/venv", "bin", "activate_this.py")
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

# Now import your app
from hub import app

application = app

