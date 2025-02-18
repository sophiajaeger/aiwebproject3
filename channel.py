from flask import Flask, request, render_template, jsonify
import json
import requests
import datetime
import openai 
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


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

CHANNELS = [
    {
        'name': 'Forum',
        'authkey': '0987654320',
        'endpoint': 'http://localhost:5001/forum',
        'file': 'forum_messages.json',
        'type_of_service': 'aiweb24:chat',
        'welcome_message': {
            'content': ('Welcome to the Travel Forum! This channel is only for travel tips and advice. '
                        'Feel free to ask about countries, continents, cities, attractions, restaurants and everything else what comes in your mind when you think about your next Trip.'), 
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
            'content': 'Welcome to your personal travel diary! Here you can save all your favourite travel moments so that only you can look at them.',
            'sender': 'System',
            'timestamp': datetime.datetime.now().isoformat(" ", "seconds"),
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
    if result.get("bad_words_total",0) > 0:
        try:
            # when testing, we realized it excluded the word beach, so we added an exception for it
            if result.get("bad_words_list").get("word").str().lower() == 'beach': 
                return False
            else:
                return True #returns true if bad word was found
        except:
            pass
    return False

# Function to generate responses
def generate_response(user_message, channel_name):
    if channel_name.lower() == 'forum':
        bot_response = generate_forum_response(user_message['content'])
        return {
            'content': bot_response,
            'sender': 'Bot',
            'timestamp': datetime.datetime.now().isoformat(" ", "seconds"),
            'extra': None
        }
    elif channel_name.lower() == 'diary':
        bot_response = generate_diary_response(user_message['sender'], user_message['content'])
        return {
            'content': bot_response,
            'sender': 'Bot',
            'timestamp': datetime.datetime.now().isoformat(" ", "seconds"),
            'extra': None
        }
    else:
        return None
    
def generate_diary_response(user, user_message):
    pass

def generate_forum_response(user_message):
    """
    Uses the OpenAI ChatCompletion API to generate a travel advice response.
    The response is conversational but may not ask follow-up questions.
    If the user's message does not appear to be related to travel or places, 
    the bot should respond with: 
    "This channel is exclusively for travel tips. Please ask a travel-related question."
    """
    
    system_prompt = (
        "You are a knowledgeable travel assistant. Provide detailed travel advice, including attractions, tips and tricks, pros and cons of destinations, and restaurant recommendations. "
        "Respond conversationally but do not ask follow-up questions. "
        "Please answer in detail with at least three complete sentences."
        "Make sure your answers always have a logical conclusion."
        "Make sure that your answer only contains full sentences and ends with a period."
        "If the user's message does not appear to be related to travel or places, respond with: "
        "'This channel is only for travel tips. Please ask a travel-related question.'"
        )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # Fallback if no API key is set (for testing)
    if not openai.api_key:
        return "This is a dummy travel response, since you did not provide an OpenAI API key. Remember to always check local reviews and ask locals for the best tips."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        # Drucke den kompletten Fehler in der Konsole, damit du ihn sehen kannst
        print("Error generating travel response:", e)
        return f"Sorry, I couldn't generate a travel response at the moment. Error: {e}"

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
    # load only messages from certain day if date_filter is active
    messages = read_messages(channel['file'], channel['welcome_message'])
    try: 
        date_filter = request.args.get('date', None)
        if date_filter:
            messages = [m for m in messages if m['timestamp'].startswith(date_filter)]
    except:
        pass
    return jsonify(messages)

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
    
    extra = 'bot_reply' # message.get('extra', None)
    if 'bot_reply' in request.form:
        extra = 'bot_reply'
        print("bot reply :)")

    # load previous messages    
    messages = read_messages(channel['file'], channel['welcome_message'])
    # filter out system messages
    messages = [m for m in messages if m['sender'] != 'System']
    # check for inappropriate content 
    if profanity_filter(message):
        system_message = {
            'content': 'Your message contained inappropriate content and was not posted.',
            'sender': 'System',
            'timestamp': datetime.datetime.now().isoformat(" ", "seconds"),
            'extra': None
        }
        messages.append(system_message)
    else:
        messages.append({'content': message['content'],
                     'sender': message['sender'],
                     'timestamp': message['timestamp'],
                     'extra': extra,
                     })
        if extra == 'bot_reply' and channel_name == 'forum':
            response = generate_response(message, channel_name)
            if response:
                messages.append(response)
    # check if messages exceed limit
    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]
    # now save message to messages file
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

if __name__ == '__main__':
    app.run(port=5001, debug=True)
