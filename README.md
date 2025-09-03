# Application-Auto-Filler
This is an application which leverages Playwright MCP Server to auto-fill any webpage(s). Here I am simulating receiving data from an external source and connecting that data to my application through a webhook. The UI is a self-made trial which can be replaced with any other UI of your choice. We can also use LLM to fill out the application form. But for user simplicity I have chosen to use javascript files and json fields to set the data in the forms. 

In this application, I have filled the registation form, the login page, selected a course and also filled its corresponding application form all with the help of Playwright MCP Server.

The flow diagram of the project is as follows:
User->>Frontend: Selects course / requests autofill
Frontend->>Agent: POST /webhook {username, course}
Agent->>Agent: Looks up the detials of the user by matching it with username and forms a user details + course JSON
Agent->>MCP Server: POST /autofill-webhook {user data}
Frontend->>MCP Server: GET /get-user-data/:username
MCP Server->>Frontend: Returns autofill JSON
Frontend->>Frontend: Autofills the form


HOW TO RUN:
Fork the repo and download the files.

Open the folder in VS CODE or any other environment

Enter into the virtual environment using in a terminal in vscode:

python -m venv venv
venv\Scripts\activate       

Ctrl + Shift + P -> Select Interpreter -> select the one ending with .venv/Scripts/python.exe 

install requirements:
pip install -r requirements.txt

install packages:
cd playwright-mcp
mpm install cors
npm install express 


create 3 terminals (ensure you are in venv) and execute in this order:

1.
cd backend
uvicorn app.main:app --reload

you should see something like:
started server process
waiting for application startup
Application Startup Complete.

2.
cd playwright-mcp
node agent.js

you should see something like:
Playwright MCP agent server running at http://localhost:4000

4.
in the project root
python test_agent.py

 * Serving Flask app 'test_agent'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001



PRESS CTRL + C TO shut down the processes in the terminal.




Create a database in PostgreSQL - autoformdb or any other name. If you are changing the name of the db, make sure you change that in the code too.

In the .env file make sure you put in your Gemini API Key if you want to use LLM for fillng up the required data.
