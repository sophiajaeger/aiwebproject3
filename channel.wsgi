import os
import sys
import traceback

sys.path.insert(1, '/home/user006/public_html/aiwebproject3>')
os.chdir('home/user006/public_html/aiwebproject3>')

@app.errorhandler(500)
def internal_error(exception):
   return "<pre>"+traceback.format_exc()+"</pre>"

from channel import app
application = app
