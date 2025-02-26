# AIWebProject3
## Name
AdventureAtlas Forum - Your AI-Powered Travel Companion

## Description
AdventureAtlas Forum is an interactive and AI-powered distributed message board designed for travel enthusiasts. It provides topic-specific discussions, AI-assisted responses to travel-related inquiries, and an open chat mode where users can communicate freely. (eventuell auch ändern wenn nur bot antwort)

Additionally, we developed an independent Java client that can connect to and interact with all available channels on the shared university server, providing a unified experience across different discussion topics

### Features
- Channel-based Messaging: Users can switch between different channels without reloading the page.
- Java Client Compatibility: Developed a Java client that works with our own channel and all other channels deployed on the shared university server.
- Login & Logout System: Authentication system integrated in the heade
- AI-Powered Responses: Utilizes OpenAI API to generate travel-related replies.
- Users can enable or disable AI-generated responses, allowing either AI-assisted replies or free chat. (eventuell raus nehmen)
- Inappropriate Content Filtering: Implements a filter API to remove offensive or irrelevant content.
- Message Limitation: A maximum of 150 messages is retained to optimize performance.
- System Messages: Displayed only until the next message is sent.

### Purpose
The project was developed as part of the course "Artificial Intelligence and the Web" by Cognitive Science Students at the University of Osnabrück.

## Instalation
### Requirements
- Python Version: 3.9 or higher
- Operating System: Windows, macOS, Linux
- Java Development Kit (JDK): Required for Java client

### Dependencies
Install required packages via requirements.txt:
```
pip install -r requirements.txt
```

Dependencies:
- Flask
- Flask-SQLAlchemy
- Requests
- OpenAI
- Python-Dotenv
- Java (for multi-channel compatibility)
- React
- Filtering API (for content moderation)

## Installation and Usage
1. Repository cloning:
    ```
    git clone https://github.com/sophiajaeger/aiwebproject3.git
    ```
2. Create and activate virtual environment:
    create a virtual enviroment:
    ```
        python -m venv myenv
    ```
    activate the enviroment:
    ```
        myenv\Scripts\activate  # Windows
        source myenv/bin/activate  # macOS/Linux
    ```
3. Install the required dependencies:
    ```
        pip install -r requirements.txt
    ```
4. Run the Channel Server:
  ```
    python channel.py
  ```
  This will start the distributed message board channel.

5. Run the React Client:

... muss noch hinzugefügt werden

6. Run the Java Client:
... muss noch hinzugefügt werden

## Support
For issues or inquiries, please contact:
Email:
- cbehr@uni-osnabrueck.de
- sjaeger@uni-osnabrueck.de
- tgrell@uni-osnabrueck.de

### Report Issues
If you have a bug or have an idea for improvement, please report it in here in GitHub Issues: https://github.com/sophiajaeger/aiwebproject3/issues 
When creating an issue, include:
  - detailed description of the problem or suggestion
  - Steps to reproduce the issue (if applicable)
  - optional: Screenshots or error messages

## Roadmap
### Future Enhancements:
- Another Channel: Diary-channel for Travel
- Enhanced Java Client: Improved UI and additional functionalities for better multi-channel interaction.

## Contributing
If you would like to contribute your own ideas, you are welcome to improve and expand AdvetureAtlas! Just follow the guideline:
1. Fork the repository
    - click the "Fork" button at the top right side of this repository to copy
2. Clone the Forked Repository
    - command to clone locally: 
    ```
    git clone https://github.com/sophiajaeger/aiwebproject3.git
    
    ```
3. Set up your enviroment
    - install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
    - set up a virtual environment: 
    ```
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
4. Create a new Branch for changes
    ```
    git checkout -b feature-branch-name
    ```
6. Dont forget to run Tests
7. Commit and push your changes
    - commit and stage your changes locally:
    ```
    git add .
    git commit -m "a short but clear description of your changes"
    ```
    - push all to GitHub:
    ```
    git push
    ```
8. Submit a Pull Request for to propose changes to the main project
    - a bunner will appear in your repository indicating that your branch is one commit before octocat:main
    - click Contribute and then Open a Pull Request
    - click on Pull Request -> include a clear description of your changes
9. Wait for an acceptance or questions about your Pull Request

A more detailed description can be found at the following link: https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project

## Authors and acknowledgment
Developed by:
- Sophia Jaeger
- Charlotte Behr
- Tuyen Grell

Lecturer of the course "Artificial Intelligence and the Web" (Universität Osnabrück): Dr. phil. Tobias Thelen 

### Project Status
Completed and deployed successfully!
