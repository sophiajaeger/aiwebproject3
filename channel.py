from flask import Flask, request, render_template, jsonify
import json
import requests
import datetime
import openai
import os

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_diary_response(user_message):
    """
    Uses the OpenAI ChatCompletion API to generate a diary-style response.
    The bot acts as a friendly diary assistant asking follow-up questions.
    """
     # Check if the API key is available 
    if not openai.api_key:
        # Fallback: Return a response for testing without Open AI
        return "This is a test response. How was your day?"
    
    system_prompt = (
        "You are a friendly diary bot that shows genuine interest in the user's day. "
        "Ask the user questions like 'How was your day?' or 'What were your highlights today?' "
        "and engage in a warm, personal conversation."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the GPT model
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response["choices"][0]["message"]["content"].strip()
        return bot_reply
    except Exception as e:
        print("Error generating diary response:", e)
        return "Sorry, I couldn't generate a response at the moment."

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
        'name': 'Africa',
        'authkey': '0987654321',
        'endpoint': 'http://localhost:5001/africa',
        'file': 'africa_messages.json',
        'type_of_service': 'aiweb24:chat',
        'welcome_message': {
            'content': 'Welcome to the Africa channel!',
            'sender': 'System',
            'timestamp': datetime.datetime.now().isoformat(),
            'extra': None
        }
    },
    {
        'name': 'Asia',
        'authkey': '0987654322',
        'endpoint': 'http://localhost:5001/asia',
        'file': 'asia_messages.json',
        'type_of_service': 'aiweb24:chat',
        'welcome_message': {
            'content': 'Welcome to the Asia channel!',
            'sender': 'System',
            'timestamp': datetime.datetime.now().isoformat(),
            'extra': None
        }
    },
    # Add more channels for other continents
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

MAX_MESSAGES = 150  # Limit to 150 messages

@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNELS

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

def check_authorization(request, channel_authkey):
    # Check if Authorization header is present and valid for the given channel
    if 'Authorization' not in request.headers:
        return False
    if request.headers['Authorization'] != 'authkey ' + channel_authkey:
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
    # Retrieve channel configuration based on channel_name
    channel = get_channel_config(channel_name)
    if not channel:
        return "Channel not found", 404

    # Check authorization using the channel's authkey
    if not check_authorization(request, channel['authkey']):
        return "Invalid authorization", 400

    # Get the message data from the request
    message = request.json
    if not message:
        return "No message", 400
    for field in ['content', 'sender', 'timestamp']:
        if field not in message:
            return f"No {field}", 400
    extra = message.get('extra', None)

    # Read current messages from the channel's file
    messages = read_messages(channel['file'], channel['welcome_message'])

    # Append the user's message
    messages.append({
        'content': message['content'],
        'sender': message['sender'],
        'timestamp': message['timestamp'],
        'extra': extra,
    })

    # If this is the Diary channel, generate a DiaryBot response
    if channel['name'].lower() == 'diary' and message['sender'].lower() != 'diarybot':
        bot_reply = generate_diary_response(message['content'])
        bot_message = {
            "content": bot_reply,
            "sender": "DiaryBot",
            "timestamp": datetime.datetime.now().isoformat(),
            "extra": None,
        }
        messages.append(bot_message)

    # Save the messages back to the file
    save_messages(messages, channel['file'])
    return "OK", 200


def read_messages(filename, welcome_message):
    """
    Reads messages from the given filename.
    If file is not found, returns a list containing the welcome message.
    """
    try:
        with open(filename, 'r') as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = [welcome_message]
    except json.decoder.JSONDecodeError:
        messages = [welcome_message]
    return messages

def save_messages(messages, filename):
    """
    Saves the messages to the given filename, limiting to MAX_MESSAGES.
    """
    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]
    with open(filename, 'w') as f:
        json.dump(messages, f)

# Start development web server
# run flask --app channel.py register
# to register channel with hub

if __name__ == '__main__':
    app.run(port=5001, debug=True)