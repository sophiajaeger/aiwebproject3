from flask import Flask, request, render_template, jsonify
import json
import requests
import datetime

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db

HUB_URL = 'http://localhost:5555'
HUB_AUTHKEY = '1234567890'
"""
CHANNEL_AUTHKEY = '0987654321'
CHANNEL_NAME = "Diary"
CHANNEL_ENDPOINT = "http://localhost:5001" # don't forget to adjust in the bottom of the file
CHANNEL_FILE = 'diary_messages.json'
CHANNEL_TYPE_OF_SERVICE = 'aiweb24:chat'
WELCOME_MESSAGE = {
    'content': 'Welcome to your personal travel diary where you can save all your favourite travel moments!',
    'sender': 'System',
    'timestamp': datetime.datetime.now().isoformat(),
    'extra': None
}
"""
CHANNELS = [
    {
        'name': 'Forum',
        'authkey': '0987654320',
        'endpoint': 'http://localhost:5001/forum',
        'file': 'africa_messages.json',
        'type_of_service': 'aiweb24:chat',
        'welcome_message': {
            'content': 'Welcome to the Forum!', # adjust !?
            'sender': 'System',
            'timestamp': datetime.datetime.now().isoformat(),
            'extra': None
        }
    },
    {
        'name': 'Diary',
        'authkey': '0987654323',
        'endpoint': 'http://localhost:5001/diary',
        'file': 'diary_messages.json',
        'type_of_service': 'aiweb24:chat',
        'welcome_message': {
            'content': 'Welcome to your personal travel diary!',
            'sender': 'System',
            'timestamp': datetime.datetime.now().isoformat(),
            'extra': None
        }
    }
]

MAX_MESSAGES = 155  # Limit to 150 messages

# filter out inappropriate messages
def filter_message(message):
    unwanted_words = ['spam', 'advertisement']
    for word in unwanted_words:
        if word in message['content'].lower():
            return False
    return True


def profanity_filter(message):
    """
    Checks if message content contains inappropriate words
    returns True if inappropriate and false if normal
    """
    url = "https://api.apilayer.com/bad_words?censor_character=censor_character"
    headers= {
        "apikey": "X22UMxBBcyIhaFPXWXDm9PH2ZxUCwqXV"
    }

    payload = message['content'].encode("utf-8")
    response = requests.post(url, headers=headers, data=payload)
    #response= requests.request("POST", url, headers=headers, data = payload)
    
    if response.status_code != 200:
        print("error from api")
        return False
    
    result = response.json()
    return result.get("bad_words_total",0) > 0 #returns true if bad word was found

# Function to generate responses
def generate_response(message):
    #if 'help' in message['content'].lower():
    return {
        'content': 'How can I assist you today?',
        'sender': 'Bot',
        'timestamp': datetime.datetime.now().isoformat(),
        'extra': None
    }
    # return None

@app.cli.command('register')
def register_command():
    global HUB_URL, HUB_AUTHKEY, CHANNELS

    for channel in CHANNELS:
        # send a POST request to server /channels
        response = requests.post(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY},
                                data=json.dumps({
                                    "name": channel['name'],
                                    "endpoint": channel['endpoint'],
                                    "authkey": channel['authkey'],
                                    "type_of_service": channel['type_of_service'],
                                 }))

        if response.status_code != 200:
            print("Error creating channel: "+str(response.status_code))
            print(response.text)
            return

def get_channel_config(name):
    for channel in CHANNELS:
        if channel['name'].lower() == name.lower():
            return channel
    return None

def check_authorization(request, authkey):
    # check if Authorization header is present
    if 'Authorization' not in request.headers:
        return False
    # check if authorization header is valid
    if request.headers['Authorization'] != 'authkey ' + authkey:
        return False
    return True
    
@app.route('/<channel_name>/health', methods=['GET'])
def health_check(channel_name):
    channel = get_channel_config(channel_name)
    if not channel:
        return "Channel not found", 404
    if not check_authorization(request, channel['authkey']):
        return "Invalid authorization", 400
    return jsonify({'name': channel['name']}), 200

# GET: Return list of messages
@app.route('/<channel_name>/', methods=['GET'])
def home_page(channel_name):
    channel = get_channel_config(channel_name)
    if not channel:
        return "Channel not found", 404
    if not check_authorization(request, channel['authkey']):
        return "Invalid authorization", 400
    return jsonify(read_messages(channel['file'], channel['welcome_message']))

# POST: Send a message
@app.route('/<channel_name>/', methods=['POST'])
def send_message(channel_name):
    # fetch channels from server
    channel = get_channel_config(channel_name)
    if not channel:
        return "Channel not found", 404
    # check authorization header
    if not check_authorization(request, channel['authkey']):
        return "Invalid authorization", 400
    # check if message is present
    message = request.json
    if not message:
        return "No message", 400
    if not 'content' in message:
        return "No content", 400
    if not 'sender' in message:
        return "No sender", 400
    if not 'timestamp' in message:
        return "No timestamp", 400
    
    extra = message.get('extra', None)
    if 'bot_reply' in request.form:
        extra = 'bot_reply'
        print("bot reply :)")

    # add message to messages
    messages = read_messages(channel['file'], channel['welcome_message'])
    # but check for inappropriate content first 
    #check for bad words with profanity filter
    if profanity_filter(message):
        system_message = {
            'content': 'Your message contained inappropriate content and was not posted.',
            'sender': 'System',
            'timestamp': datetime.datetime.now().isoformat(),
            'extra': None
        }
        messages.append(system_message)
    else:
        messages.append({'content': message['content'],
                     'sender': message['sender'],
                     'timestamp': message['timestamp'],
                     'extra': extra,
                     })
        if extra == 'bot_reply':
            response = generate_response(message)
            if response:
                messages.append(response)
    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]
    save_messages(channel['file'], messages)
    return "OK", 200

def read_messages(file, welcome_message):
    try:
        with open(file, 'r') as f:
            messages = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messages = [welcome_message]
    return messages

def save_messages(file, messages):
    with open(file, 'w') as f:
        json.dump(messages, f)

# Start development web server
# run flask --app channel.py register
# to register channel with hub

if __name__ == '__main__':
    app.run(port=5001, debug=True)
